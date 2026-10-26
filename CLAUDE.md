# QLDT Project Harness

## Project

Course registration and academic management system for IT3180. The repository is divided into contracts, backend, frontend, database, documentation, gateway, CI/CD, and end-to-end tests.

## Source of truth

- Read `docs/00-INDEX.md` to find the right project document.
- The supplied FE-BE API conventions take precedence over older design notes.
- `contracts/openapi.yaml` is the final API contract when the backend team adds it. Do not invent request/response fields while it is absent.
- SQL schema and seed now live under `db/`; see `db/README.md` for setup.
- Backend is FastAPI + SQLAlchemy + Alembic under `backend/app/`; migrations must preserve the uppercase SQL table names in `db/schema.sql`.
- `backend/CLAUDE.md` is the backend-specific harness. Catalog and timetable service operations remain scaffolds returning `501 NOT_IMPLEMENTED`; registration register/cancel/list are implemented.
- `docker-compose.yml` is the local stack entry point; `.github/workflows/ci-cd.yml` runs backend checks, migrations, and gateway smoke tests.

## Working rules

- Frontend lives in `frontend/`; backend work belongs to the backend owner. The API application and tests live under `backend/app/` and `backend/tests/`.
- Keep API names, camelCase JSON keys, UPPER_SNAKE_CASE enums, error codes, and `/api` base path aligned with the contract.
- The server owns registration eligibility, conflicts, and seat counts. Refetch after mutations; never adjust enrollment counts locally.
- A 401 clears the session and returns to login. A 403 shows an access error without logging out.
- Never expose passwords, password hashes, tokens, SQL, or stack traces in UI/logs.
- Treat assumptions as temporary, isolate them, and replace them when `contracts/openapi.yaml` is available. FastAPI's generated `/api/openapi.json` is not a substitute for that reviewed contract.

## Commands

```bash
cd frontend
npm install
npm run dev
npm run build
```

Backend checks:

```powershell
cd backend
pip install -r requirements-dev.txt
ruff check .
pytest
```

See `backend/CLAUDE.md`, `frontend/CLAUDE.md`, and `README.md` for component setup and current status.