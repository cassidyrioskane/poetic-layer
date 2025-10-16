# services/mapping_service/app.py
from threading import Thread
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import os, time, uuid, json
from services.mapping_service import seed, mappings

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
MOTIFS_PATH = os.path.join(DATA_DIR, "motifs.json")
MAPPINGS_PATH = os.path.join(DATA_DIR, "mappings.json")

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

# ---------- In-memory stores ----------
MOTIFS: Dict[str, Dict[str, Any]] = {}
MAPPINGS: Dict[str, Dict[str, Any]] = {}

# ---------- Persistence ----------
def save_state():
    try:
        with open(MOTIFS_PATH, "w", encoding="utf-8") as f:
            json.dump(MOTIFS, f, ensure_ascii=False, indent=2)
        with open(MAPPINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(MAPPINGS, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[persist] Failed to save state: {e}")

def load_state():
    try:
        if os.path.exists(MOTIFS_PATH):
            with open(MOTIFS_PATH, "r", encoding="utf-8") as f:
                MOTIFS.update(json.load(f))
        if os.path.exists(MAPPINGS_PATH):
            with open(MAPPINGS_PATH, "r", encoding="utf-8") as f:
                MAPPINGS.update(json.load(f))
        if MOTIFS:
            print(f"[persist] Loaded {len(MOTIFS)} motifs from disk.")
        if MAPPINGS:
            print(f"[persist] Loaded {len(MAPPINGS)} mappings from disk.")
    except Exception as e:
        print(f"[persist] Failed to load state: {e}")

# ---------- Automatic Seeding ----------
@app.on_event("startup")
def auto_seed():
    """
    Automatically load saved motifs, then seed defaults if none exist.
    Ensures the app always has base content, even after restarts.
    """
    load_state()

    def _seed_async():
        time.sleep(1.0)
        try:
            if not MOTIFS:
                seed.seed_if_empty()
                save_state()
        except Exception as e:
            print(f"[startup] Seeding failed: {e}")

    Thread(target=_seed_async, daemon=True).start()

# ---------- CORS ----------
GITHUB_USER = "cassidyrioskane"
REPO_NAME = "poetic-layer"

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    f"https://{GITHUB_USER}.github.io",
    f"https://{GITHUB_USER}.github.io/{REPO_NAME}",
    "https://poetic-layer-backend.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Helpers ----------
def _ensure_motif_dict(payload: Dict[str, Any]) -> Dict[str, Any]:
    mid = payload.get("id") or str(uuid.uuid4())
    name = payload.get("name") or "Untitled"

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
    save_state()
    return m

@app.delete("/motifs/{motif_id}")
def delete_motif(motif_id: str):
    if motif_id in MOTIFS:
        del MOTIFS[motif_id]
        save_state()
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

    if src.get("type") == "text" and "text" not in src and "content" in src:
        src = dict(src)
        src["text"] = src["content"]

    func = mappings.MAPPING_REGISTRY.get(mtype)
    print(f"[run_mapping] Executing: {mtype} -> {func}")
    if not func:
        raise HTTPException(404, f"Unknown mapping type: {mtype}")

    try:
        out_text = func(src, params)
    except Exception as e:
        raise HTTPException(500, f"Mapping '{mtype}' failed: {e}")

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
    save_state()

    metrics = {"runtime_s": 0.0, "mapping_type": mtype, "source_id": src["id"]}
    return {"output": out, "metrics": metrics}
