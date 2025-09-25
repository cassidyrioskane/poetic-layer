from fastapi import FastAPI
from packages.schemas.models import Motif, MappingSpec

app = FastAPI(title="Mapping Service")

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
