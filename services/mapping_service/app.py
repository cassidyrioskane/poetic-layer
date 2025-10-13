# services/mapping_service/app.py
from threading import Thread
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import os, time, uuid
from services.mapping_service import seed, mappings


# ---------- Models ----------
try:
    from packages.schemas.models import Motif, MappingSpec  # type: ignore
except Exception:
    from pydantic import BaseModel
    from typing import List, Dict, Any

    class Motif(BaseModel):
        id: str
        name: str
        text: str = ""
        tags: List[str] = []
        ethics: Dict[str, Any] = {}
        version: str = "1.0"
        provenance: Dict[str, Any] = {}
        type: str = "text"
        content: str | None = None

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
    """
    Automatically seed default motifs and image motifs on startup.
    Ensures the app always has base content, even after container restarts.
    """
    def _seed_async():
        time.sleep(1.0)  # delay so server is live
        try:
            seed.seed_if_empty()
        except Exception as e:
            print(f"[startup] Seeding failed: {e}")

    Thread(target=_seed_async, daemon=True).start()


# ---------- CORS ----------
GITHUB_PAGES_URL = "https://cassidyrioskane.github.io"
GITHUB_REPO_URL = f"{GITHUB_PAGES_URL}/poetic-layer"  # replace with your repo name exactly

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        GITHUB_PAGES_URL,
        GITHUB_REPO_URL,
        "https://poetic-layer-backend.onrender.com",
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

    # Handle image vs text
    if payload.get("type") == "image" or "image_data" in payload:
        mtype = "image"
        content = payload.get("content") or payload.get("image_data")
        text = ""
    else:
        mtype = "text"
        text = payload.get("content") or payload.get("text") or ""
        content = None

    return {
        "id": mid,
        "name": name,
        "type": mtype,
        "text": text,
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


# ---------- Mapping Registry ----------
@app.get("/mappings")
def list_mappings():
    from services.mapping_service.mappings import MAPPING_META
    return [{"type": name, "description": meta["description"]} for name, meta in MAPPING_META.items()]


@app.get("/registry/mappings")
def list_registry_mappings():
    from services.mapping_service.mappings import MAPPING_META
    return [
        {
            "type": name,
            "description": meta.get("description", "No description available."),
            "domain": meta.get("domain", "text"),
        }
        for name, meta in MAPPING_META.items()
    ]


# ---------- Execute a Mapping ----------
@app.post("/mappings/run")
def run_mapping(spec_payload: Dict[str, Any] = Body(...)):
    mtype = spec_payload.get("type")
    signature = spec_payload.get("signature") or {}
    params = spec_payload.get("params") or {}
    input_id = signature.get("input_motif_id")

    if not input_id:
        raise HTTPException(422, "signature.input_motif_id is required")

    src = MOTIFS.get(input_id)
    if not src:
        raise HTTPException(404, "Input motif not found")

    func = mappings.MAPPING_REGISTRY.get(mtype)
    print(f"[run_mapping] Executing: {mtype} -> {func}")

    if not func:
        raise HTTPException(404, f"Unknown mapping type: {mtype}")

    try:
        out_text = func(src, params)
    except Exception as e:
        raise HTTPException(500, f"Mapping '{mtype}' failed: {e}")

    # Detect image output (base64-encoded image data)
    if isinstance(out_text, str) and out_text.strip().startswith("iVBOR"):
        motif_type = "image"
        motif_field = {"content": out_text}
    else:
        motif_type = "text"
        motif_field = {"text": out_text}

    out = _ensure_motif_dict({
        "name": f"{src['name']} :: {mtype}",
        "type": motif_type,
        **motif_field,
        "tags": src.get("tags", []),
        "ethics": src.get("ethics", {}),
        "provenance": {
            "who": "mapping-service",
            "when": int(time.time()),
            "source_ref": src["id"],
            "source_name": src["name"],
            "source_type": src.get("type", "text"),
        },
    })
    MOTIFS[out["id"]] = out

    return {
        "output": out,
        "metrics": {
            "runtime_s": 0.0,
            "mapping_type": mtype,
            "source_id": src["id"],
        },
    }
