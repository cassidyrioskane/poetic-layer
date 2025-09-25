from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from packages.schemas.models import Motif, MappingSpec

app = FastAPI(title="Mapping Service")
frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:3000")

# Enable CORS so frontend can access this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],  # frontend dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

MOTIFS = {}
MAPPINGS = {}

# ---- SEED ----
from .seed import seed_data
seed_data()
# --------------

@app.post("/motifs")
def create_motif(motif: Motif):
    MOTIFS[motif.id] = motif
    return motif

@app.get("/motifs")
def list_motifs():
    """Return all motifs"""
    return list(MOTIFS.values())

@app.get("/motifs/{motif_id}")
def get_motif(motif_id: str):
    return MOTIFS.get(motif_id)

@app.post("/mappings")
def create_mapping(spec: MappingSpec):
    MAPPINGS[spec.id] = spec
    return spec

@app.get("/mappings/{mapping_id}")
def get_mapping(mapping_id: str):
    return MAPPINGS.get(mapping_id)
