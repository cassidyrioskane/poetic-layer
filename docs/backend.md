# Backend (Mapping Service)

## FastAPI Endpoints
- `POST /motifs`: Create a new motif
- `GET /motifs`: List all motifs
- `GET /motifs/{motif_id}`: Get motif by ID
- `POST /mappings`: Create a new mapping
- `GET /mappings/{mapping_id}`: Get mapping by ID

## Schemas
- **Motif**: ID, name, text, tags, ethics, version, provenance
- **MappingSpec**: ID, motif_id, type, signature, constraints, codegen_ref, params_schema, tests, score, version
- **LedgerEntry**: Tracks run results, metrics, and decisions

## Dependencies
- `fastapi`
- `pydantic`
- `uvicorn`
