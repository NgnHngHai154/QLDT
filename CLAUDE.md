# QLDT Project Harness

## Project

Course registration and academic management system for IT3180. The repository is divided into contracts, backend, frontend, database, documentation, and end-to-end tests.

## Source of truth

- Read `docs/00-INDEX.md` to find the right project document.
- The supplied FE-BE API conventions take precedence over older design notes.
- `contracts/openapi.yaml` is the final API contract when the backend team adds it. Do not invent request/response fields while it is absent.
- SQL schema and seed now live under `db/`; see `db/README.md` for setup.

## Working rules

- Frontend lives in `frontend/`; backend work belongs to the backend owner.
- Keep API names, camelCase JSON keys, UPPER_SNAKE_CASE enums, error codes, and `/api` base path aligned with the contract.
- The server owns registration eligibility, conflicts, and seat counts. Refetch after mutations; never adjust enrollment counts locally.
- A 401 clears the session and returns to login. A 403 shows an access error without logging out.
- Never expose passwords, password hashes, tokens, SQL, or stack traces in UI/logs.
- Treat assumptions as temporary, isolate them, and replace them when OpenAPI is available.

## Commands

```bash
cd frontend
npm install
npm run dev
npm run build
```

See `frontend/CLAUDE.md` for FE rules and `README.md` for onboarding/status.