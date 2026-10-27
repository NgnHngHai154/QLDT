# QLDT Project Harness

## Project

Course registration and academic management system for IT3180. The repository is divided into contracts, backend, frontend, database, documentation, gateway, CI/CD, and end-to-end tests.

## Source of truth

- Read `docs/00-INDEX.md` to find the right project document.
- The supplied FE-BE API conventions take precedence over older design notes.
- `contracts/openapi.yaml` and `contracts/api-types.ts` define the official API contract and shared TypeScript types for frontend and backend.
- SQL schema and seed live under `db/`; see `db/README.md` for setup.
- Backend is FastAPI + SQLAlchemy + Alembic under `backend/app/`; migrations preserve the uppercase SQL table names in `db/schema.sql`.
- `backend/CLAUDE.md` is the backend-specific harness. Business services for UC001-UC009 are implemented; registration operates on a single active semester, enforces credit limits, and serializes registration changes. Prerequisite and corequisite checks are excluded.
- `docker-compose.yml` is the local stack entry point; `.github/workflows/ci-cd.yml` runs backend checks, migrations, and gateway smoke tests.

## Working rules

- Frontend lives in `frontend/`; backend work belongs to the backend owner. The API application and tests live under `backend/app/` and `backend/tests/`.
- Keep API names, camelCase JSON keys, UPPER_SNAKE_CASE enums, error codes, and `/api` base path aligned with the contract.
- The server owns registration eligibility, conflicts, and seat counts. Refetch after mutations; never adjust enrollment counts locally.
- A 401 clears the session and returns to login. A 403 shows an access error without logging out.
- Never expose passwords, password hashes, tokens, SQL, or stack traces in UI/logs.

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
