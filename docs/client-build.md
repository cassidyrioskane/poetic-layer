
---

## **5. `docs/client-build.md` – Client Build Instructions**

```markdown
# Client Build

This folder contains prebuilt frontend and backend for clients who do not use Docker.

## Running the App
- **Mac:** `./run-client-build.sh`
- **Windows:** `run-client-build.bat`

## Updating Builds
- Run `./update-client-build.sh` from the root project folder.
- This rebuilds the frontend, copies the mapping service, and updates the scripts.

## Notes
- Frontend is served at `http://localhost:80`
- Mapping service runs internally; client does not need to access it directly.
