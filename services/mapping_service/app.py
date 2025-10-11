from threading import Thread
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import os, time, uuid
from services.mapping_service import seed
from services.mapping_service import mappings

# ---------- Models ----------
try:
    from packages.schemas.models import Motif, MappingSpec  # type: ignore
except Exception:
    # Minimal fallback models so this file runs even if packaging paths shift.
    from pydantic import BaseModel
    from typing import List, Dict, Any

    class Motif(BaseModel):
        id: str
        name: str
        text: str
        tags: List[str] = []
        ethics: Dict[str, Any] = {}
        version: str = "1.0"
        provenance: Dict[str, Any] = {}

    class MappingSpec(BaseModel):
        id: str
        type: str
        signature: Dict[str, Any] = {}
        constraints: Dict[str, Any] = {}
        params_schema: Dict[str, Any] = {}
        tests: list = []
        codegen_ref: str | None = None
        score: float | None = None
        version: str = "1.0"


# ---------- Setup ----------
mappings.discover_mappings()

app = FastAPI(title="Mapping Service (Poetic Layer)")


# ---------- Automatic Seeding ----------
@app.on_event("startup")
def auto_seed():
    """Run seeding asynchronously after app startup."""
    def _seed_async():
        # small delay to ensure endpoints are live
        time.sleep(1.0)
        seed.seed_if_empty()
    Thread(target=_seed_async, daemon=True).start()


# ---------- CORS ----------
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://127.0.0.1:3000",
        "http://frontend",
        "http://frontend:80",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- In-memory stores ----------
MOTIFS: Dict[str, Dict[str, Any]] = {}
MAPPINGS: Dict[str, Dict[str, Any]] = {}


# ---------- Helpers ----------
def _ensure_motif_dict(payload: Dict[str, Any]) -> Dict[str, Any]:
    mid = payload.get("id") or str(uuid.uuid4())
    name = payload.get("name") or "Untitled"
    if "image_data" in payload or payload.get("type") == "image":
        mtype = "image"
        content = payload.get("content") or payload.get("image_data")
    else:
        mtype = "text"
        content = payload.get("content") or payload.get("text") or ""
    return {
        "id": mid,
        "name": name,
        "type": mtype,
        "content": content,
        "tags": payload.get("tags", []),
        "ethics": payload.get("ethics", {}),
        "version": payload.get("version", "1.0"),
        "provenance": payload.get("provenance", {"who": "ui", "when": int(time.time())}),
    }



def _motif_model(m: Dict[str, Any]) -> Motif:
    return Motif(**m)  # type: ignore


# ---------- Motif Endpoints ----------
@app.get("/motifs")
def list_motifs():
    return list(MOTIFS.values())


@app.get("/motifs/{motif_id}")
def get_motif(motif_id: str):
    m = MOTIFS.get(motif_id)
    if not m:
        raise HTTPException(404, "Motif not found")
    return m


@app.post("/motifs")
def create_motif(motif_payload: Dict[str, Any] = Body(...)):
    m = _ensure_motif_dict(motif_payload)
    MOTIFS[m["id"]] = m
    return m


@app.delete("/motifs/{motif_id}")
def delete_motif(motif_id: str):
    if motif_id in MOTIFS:
        del MOTIFS[motif_id]
    return {"ok": True}


# ---------- Mapping Spec Endpoints ----------
@app.get("/mappings")
def list_mappings():
    from services.mapping_service.mappings import MAPPING_META
    return [
        {"type": name, "description": meta["description"]}
        for name, meta in MAPPING_META.items()
    ]



@app.get("/mappings/{mapping_id}")
def get_mapping(mapping_id: str):
    spec = MAPPINGS.get(mapping_id)
    if not spec:
        raise HTTPException(404, "Mapping not found")
    return spec


@app.post("/mappings")
def create_mapping(spec_payload: Dict[str, Any] = Body(...)):
    # Accept flexible payload; enforce id/type minimally
    if "id" not in spec_payload:
        spec_payload["id"] = str(uuid.uuid4())
    if "type" not in spec_payload:
        raise HTTPException(422, "Mapping 'type' is required")
    spec_payload.setdefault("signature", {})
    spec_payload.setdefault("constraints", {})
    spec_payload.setdefault("params_schema", {})
    spec_payload.setdefault("tests", [])
    spec_payload.setdefault("version", "1.0")
    MAPPINGS[spec_payload["id"]] = spec_payload
    return spec_payload

# --- Registry (discovered mapping functions + docstrings) ---
@app.get("/registry/mappings")
def list_registry_mappings():
    from services.mapping_service.mappings import MAPPING_META
    return [
        {"type": name, "description": meta.get("description", "No description available.")}
        for name, meta in MAPPING_META.items()
    ]


# ---------- Execute a Mapping ----------
@app.post("/mappings/run")
def run_mapping(spec_payload: Dict[str, Any] = Body(...)):
    """
    Executes any registered mapping function on the given motif.
    Uses the global mappings.MAPPING_REGISTRY rather than hard-coded demos.
    """
    mtype = spec_payload.get("type")
    signature = spec_payload.get("signature") or {}
    params = spec_payload.get("params") or {}
    input_id = signature.get("input_motif_id")
    if not input_id:
        raise HTTPException(422, "signature.input_motif_id is required")

    src = MOTIFS.get(input_id)
    if not src:
        raise HTTPException(404, "Input motif not found")

    # --- Dynamic dispatch using registered mappings ---
    func = mappings.MAPPING_REGISTRY.get(mtype)
    print(f"RUN_MAPPING: type={mtype}, func={func}")

    if not func:
        raise HTTPException(404, f"Unknown mapping type: {mtype}")

    try:
        out_text = func(src, params)
    except Exception as e:
        raise HTTPException(500, f"Mapping '{mtype}' failed: {e}")

    out = _ensure_motif_dict({
        "name": f"{src['name']} :: {mtype}",
        "text": out_text,
        "tags": src.get("tags", []),
        "ethics": src.get("ethics", {}),
        "provenance": {
            "who": "mapping-service",
            "when": int(time.time()),
            "source_ref": src["id"],
        },
    })
    MOTIFS[out["id"]] = out

    metrics = {
        "runtime_s": 0.0,
        "mapping_type": mtype,
        "source_id": src["id"],
    }

    return {"output": out, "metrics": metrics}
