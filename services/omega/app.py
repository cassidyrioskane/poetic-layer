from fastapi import FastAPI
from pydantic import BaseModel
from packages.policy.engine import OmegaPolicyEngine

app = FastAPI(title="Omega Governance Service")
engine = OmegaPolicyEngine("packages/policy/policies.yaml")

class Metrics(BaseModel):
    coherence_tech: float
    coherence_poetic: float
    nli_contradiction: float
    ethics_risk: float
    calibration_error: float = 0.0
    runtime_s: float = 0.0

@app.post("/govern")
def govern(metrics: Metrics):
    decision = engine.govern(metrics.dict())
    return {"decision": decision}
