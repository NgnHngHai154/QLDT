# Backend Rules

- Runtime: Python 3.12+, FastAPI, SQLAlchemy 2, and Alembic; application package root is `app/`.
- Start locally with `uvicorn app.main:app --reload` from `backend/`.
- Authentication reads the canonical MySQL `USERS` table; production code must not fall back to fixture/mock users.
- `db/schema.sql` and `db/seed/seed.sql` remain the database source of truth. ORM table identifiers and Alembic migrations must preserve their uppercase names and use database `qldt`.
- Keep one ADMIN seed account only. Sample credentials are documented in `db/README.md`.
- JWT access token lifetime is 3600 seconds; do not add refresh tokens unless the SRS/API contract changes.
- `JWT_SECRET` is required and must be at least 32 characters. Semester credit limits are system-wide environment settings (`MIN_CREDITS_PER_SEMESTER=12`, `MAX_CREDITS_PER_SEMESTER=24` by default); maximum must be >= 1 and >= minimum. These are temporary defaults pending group confirmation.
- Registration/cancellation lock the student's row with `SELECT ... FOR UPDATE` before checking credit and schedule rules. Credit totals sum `SUBJECTS.credits` for registrations in the semester; prerequisite and co-requisite checks are out of scope.
- All API routes use `/api`; JSON keys are camelCase and errors use the shared FE-BE envelope. Auth returns `accessToken` and a nested `user` object for FE compatibility.
- Business modules belong in `app/{controller,service,repository,entity,dto}/{auth,catalog,registration,timetable}`; shared configuration and errors belong in `app/core/`, and authentication helpers belong in `app/security/`.
- Catalog and timetable services that still raise `NotImplementedError` return `501 NOT_IMPLEMENTED`. Registration, cancellation, and list-mine are implemented and have SQLite-backed tests. Compose startup and MySQL migration were verified, but registration rules and concurrent MySQL row locking still need dedicated verification.
- Run `ruff check .`, `pytest`, `alembic upgrade head`, and `alembic check` from `backend/`. CI also builds and smoke-tests the Compose gateway stack.
- Keep `contracts/openapi.yaml` synchronized with backend routes when the reviewed FE-BE contract is added; generated FastAPI docs are not its replacement.
