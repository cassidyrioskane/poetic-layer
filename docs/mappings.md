# Mappings

## What are Mappings?
Mappings define how motifs interact with one another or with external processes. They include:
- Type: e.g., "ode", "pde", "data_labeler"
- Signature: input/output structure
- Constraints: rules or conditions
- Params Schema: configurable parameters
- Tests: validation rules
- Score: numerical evaluation

## Example Mapping JSON
```json
{
  "id": "mapping-001",
  "motif_id": "motif-001",
  "type": "ode",
  "signature": {"input": "text", "output": "vector"},
  "constraints": {"length": "max 100"},
  "codegen_ref": "codegen-v1",
  "params_schema": {},
  "tests": [],
  "score": 0.85,
  "version": "1.0"
}
