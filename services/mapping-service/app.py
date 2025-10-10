from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import os, time, uuid
from services.mapping_service import mappings

# If your repo already has these models, we keep the import.
# If fields differ, we coerce inputs below to avoid 422s.
try:
    from packages.schemas.models import Motif, MappingSpec  # type: ignore
except Exception:
    # Minimal fallback models so this file runs even if packaging paths shift.
    from pydantic import BaseModel, Field
    from typing import List, Optional, Dict

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


mappings.discover_mappings()

app = FastAPI(title="Mapping Service (Poetic Layer)")

# ---- CORS ----
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://127.0.0.1:3000",
        "http://frontend",       # 👈 container hostname
        "http://frontend:80"     # 👈 explicit port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- In-memory stores ----
MOTIFS: Dict[str, Dict[str, Any]] = {}
MAPPINGS: Dict[str, Dict[str, Any]] = {}

# ---------- Helpers ----------
def _ensure_motif_dict(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Accept flexible user input and coerce to a Motif-compatible dict.
    Required: name, text. We generate id and defaults if missing.
    """
    mid = payload.get("id") or str(uuid.uuid4())
    name = payload.get("name") or payload.get("title") or "Untitled"
    text = payload.get("text") or payload.get("description") or ""
    tags = payload.get("tags") or []
    ethics = payload.get("ethics") or {}
    version = payload.get("version") or "1.0"
    provenance = payload.get("provenance") or {"who": "ui", "when": int(time.time())}
    return {
        "id": mid,
        "name": name,
        "text": text,
        "tags": tags,
        "ethics": ethics,
        "version": version,
        "provenance": provenance,
    }

def _motif_model(m: Dict[str, Any]) -> Motif:
    return Motif(**m)  # type: ignore

# ---------- Motifs ----------
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

# ---------- Mappings (spec registry) ----------
@app.get("/mappings")
def list_mappings():
    return list(MAPPINGS.values())

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

# ---------- Execute a mapping ----------
@app.post("/mappings/run")
def run_mapping(spec_payload: Dict[str, Any] = Body(...)):
    """
    Minimal built-in executor so you can test mappings immediately.
    Expects spec.signature.input_motif_id, and supports a few demo types:
      - 'uppercase' : output.text = input.text.upper()
      - 'append'    : output.text = input.text + params.append_text
      - 'echo'      : copies input text
    Returns: {"output": Motif, "metrics": {...}}
    """
    # spec basics
    mtype = spec_payload.get("type")
    signature = spec_payload.get("signature") or {}
    params = spec_payload.get("params") or {}
    input_id = signature.get("input_motif_id")
    if not input_id:
        raise HTTPException(422, "signature.input_motif_id is required")

    src = MOTIFS.get(input_id)
    if not src:
        raise HTTPException(404, "Input motif not found")

    src_text = src.get("text", "")

    if mtype == "uppercase":
        out_text = src_text.upper()
    elif mtype == "append":
        out_text = src_text + str(params.get("append_text", ""))
    elif mtype == "echo":
        out_text = src_text
    else:
        # Unknown mapping type → no-op
        out_text = src_text

    out = _ensure_motif_dict({
        "name": f"{src['name']} :: {mtype or 'noop'}",
        "text": out_text,
        "tags": src.get("tags", []),
        "ethics": src.get("ethics", {}),
        "provenance": {"who": "mapping-service", "when": int(time.time()), "source_ref": src["id"]},
    })
    MOTIFS[out["id"]] = out

    metrics = {
        "runtime_s": 0.0,
        "mapping_type": mtype or "noop",
        "source_id": src["id"],
    }

    return {"output": out, "metrics": metrics}
