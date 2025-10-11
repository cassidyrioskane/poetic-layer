from pydantic import BaseModel, AnyUrl
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime

class Motif(BaseModel):
    id: str
    name: str
    type: str = "text"           # "text" or "image"
    content: str                 # text body or base64-encoded image
    tags: List[str] = []
    ethics: Dict[str, Any] = {}
    version: str = "1.0"
    provenance: Dict[str, Any] = {}

class MappingSpec(BaseModel):
    id: str
    motif_id: str
    type: Literal["ode","pde","bc","regularizer","data_labeler","search_operator"]
    signature: Dict[str, str]
    constraints: Dict[str, str]
    codegen_ref: str
    params_schema: Dict
    tests: List[Dict]
    score: float
    version: str

class RunMetrics(BaseModel):
    loss: Optional[float] = None
    coherence_tech: float
    coherence_poetic: float
    nli_contradiction: float
    ethics_risk: float
    calibration_error: Optional[float] = None
    runtime_s: float

class LedgerEntry(BaseModel):
    id: str
    t: int
    motifs: List[str]
    specs: List[str]
    explanations: Dict[str, str]
    artifacts: Dict[str, AnyUrl]
    metrics: RunMetrics
    decision: Literal["keep","revise","collapse"]
    parent_id: Optional[str]
    created_at: datetime
