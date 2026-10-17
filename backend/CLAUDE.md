# Backend Rules

- Runtime: Python 3.11+, Sanic, package root `src/qldt/`.
- Authentication reads the canonical MySQL `USERS` table; production code must not fall back to fixture/mock users.
- Keep one ADMIN seed account only. Sample credentials are documented in `db/README.md`.
- JWT access token lifetime is 3600 seconds; do not add refresh tokens unless the SRS/API contract changes.
- All API routes use `/api`; JSON keys are camelCase and errors use the shared FE-BE envelope.
- Business modules belong in `src/qldt/{auth,catalog,registration,timetable,security,common}`.
- Run `pytest` and keep `contracts/openapi.yaml` synchronized with backend routes.