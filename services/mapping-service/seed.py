from packages.schemas.models import Motif, MappingSpec
from .app import MOTIFS, MAPPINGS

def seed_data():
    motif = Motif(
        id="twinned_lullaby",
        name="Twinned Lullaby",
        text="Two voices weave together, oscillating in fragile balance.",
        tags=["oscillator", "symmetry"],
        ethics={"risk_tags": [], "jurisdictions": []},
        version="1.0.0",
        provenance={"author": "system", "source": "seed"}
    )

    mapping = MappingSpec(
        id="coupled_oscillators",
        motif_id="twinned_lullaby",
        type="ode",
        signature={"y": "R^4 -> R^4"},
        constraints={"energy": "bounded"},
        codegen_ref="coupled_oscillators.py.j2",
        params_schema={
            "type": "object",
            "properties": {
                "k": {"type": "number", "default": 1.0},
                "c": {"type": "number", "default": 0.0},
                "k_c": {"type": "number", "default": 0.1}
            }
        },
        tests=[{"name": "energy_bound", "assert": "max(E) < 100"}],
        score=0.9,
        version="1.0.0"
    )

    MOTIFS[motif.id] = motif
    MAPPINGS[mapping.id] = mapping
    print("✅ Seeded Registry with twinned_lullaby + coupled_oscillators")

# Run seeder if this script is executed directly
if __name__ == "__main__":
    seed_data()
