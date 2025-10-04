
---

## **2. `docs/frontend.md` – Frontend Documentation**

```markdown
# Frontend

## Component Overview
The main component is `MotifManager.js`, which allows users to:
- View all existing motifs
- Create new motifs
- Edit motifs (future feature)

Other components:
- App.js / App.jsx: Main entry point
- index.js: React root

### API Integration
All frontend-backend communication goes through `api.js`. Key functions:
- `getMotifs()`: Retrieve all motifs
- `createMotif(motif)`: Save a new motif
- Future functions: `getMappings()`, `createMapping()`, etc.

### Forms
- Required fields are enforced before submission.
- Error handling for invalid data is implemented via React state.

### State & Props
- `MotifManager` maintains local state for motif lists.
- Updates propagate to UI automatically after API responses.
