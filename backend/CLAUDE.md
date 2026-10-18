# Backend Rules

- Runtime: Python 3.12+, FastAPI, SQLAlchemy 2, and Alembic; application package root is `app/`.
- Start locally with `uvicorn app.main:app --reload` from `backend/`.
- Authentication reads the canonical MySQL `USERS` table; production code must not fall back to fixture/mock users.
- `db/schema.sql` and `db/seed/seed.sql` remain the database source of truth. ORM table identifiers and Alembic migrations must preserve their uppercase names and use database `qldt`.
- Keep one ADMIN seed account only. Sample credentials are documented in `db/README.md`.
- JWT access token lifetime is 3600 seconds; do not add refresh tokens unless the SRS/API contract changes.
- All API routes use `/api`; JSON keys are camelCase and errors use the shared FE-BE envelope. Auth returns `accessToken` and a nested `user` object for FE compatibility.
- Business modules belong in `app/{controller,service,repository,entity,dto}/{auth,catalog,registration,timetable}`; shared configuration and errors belong in `app/core/`, and authentication helpers belong in `app/security/`.
- Catalog, registration, and timetable services that still raise `NotImplementedError` return `501 NOT_IMPLEMENTED`. Do not report these capabilities as implemented until the business logic and tests exist.
- Run `ruff check .`, `pytest`, `alembic upgrade head`, and `alembic check` from `backend/`. CI also builds and smoke-tests the Compose gateway stack.
- Keep `contracts/openapi.yaml` synchronized with backend routes when the reviewed FE-BE contract is added; generated FastAPI docs are not its replacement.
