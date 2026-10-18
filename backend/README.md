# Backend API – QLDT

Python 3.12 · FastAPI · SQLAlchemy 2 · Alembic · MySQL 8 · JWT + Bcrypt.

The reviewed FE-BE conventions take precedence over older design notes. The canonical SQL schema and seed remain under `../db/`; `contracts/openapi.yaml` is still pending. The generated FastAPI document at `/api/openapi.json` describes the current implementation, not an approved replacement contract.

## Local run

From the repository root, start the MySQL service:

```powershell
docker compose up -d db
```

Then, from this directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
Copy-Item .env.example .env
alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload
```

The example `.env` targets the local Compose database `qldt` using its development-only `app` credentials. Set a unique `JWT_SECRET` of at least 32 characters outside local development.

- API docs: `http://localhost:8000/api/docs`
- API OpenAPI JSON: `http://localhost:8000/api/openapi.json`
- Health: `http://localhost:8000/health`

The optional idempotent dev seed creates `admin / admin`, `gv001 / 123456`, and `sv20210001 / 123456`. For the full project sample database, use `../db/seed/seed.sql` as documented in `../db/README.md`; do not expose sample credentials in production.

## Tests and migrations

From `backend/`, run:

```powershell
ruff check .
pytest
alembic upgrade head
alembic check
```

Pytest uses an in-memory SQLite database and does not require MySQL. Migration commands require a MySQL database at `DATABASE_URL`; CI runs them against MySQL 8.4. ORM and Alembic table names stay uppercase to match `db/schema.sql` on case-sensitive MySQL hosts.

When changing entities, create and review a migration with `alembic revision --autogenerate -m "describe change"`, then verify `alembic upgrade head` and `alembic check`.

## Architecture

```
app/
├─ controller/   HTTP routes, request validation, response DTOs
├─ service/      business rules and transaction boundaries
├─ repository/   database queries
├─ entity/       SQLAlchemy mapping for the eight canonical tables
├─ dto/          input/output schemas and common responses
├─ security/     JWT, password hashing, role dependencies
└─ core/         settings, database sessions, errors, time handling
```

Keep dependencies flowing `controller → service → repository → entity`. Services own business behavior and commit writes only after successful operations.

## Current API implementation status

Implemented and covered by tests: login, current user, logout, role checks, health handling, and semester list/current lookup.

The subject, section, registration, and timetable services are scaffolds; their unimplemented operations deliberately return `501 NOT_IMPLEMENTED`. Routes, DTOs, repositories, and some query helpers are present, but the business use cases are not complete and should remain marked pending in [../tasks/BOARD.md](../tasks/BOARD.md).

The login response uses `accessToken` and nested camelCase `user` data, matching the current frontend adapter. Verify all API details against the reviewed OpenAPI contract when it is added.

## CI/CD and local deployment

- Root [docker-compose.yml](../docker-compose.yml) starts MySQL, the backend, and the gateway.
- [../gateway/README.md](../gateway/README.md) documents gateway behavior and its smoke test.
- [.github/workflows/ci-cd.yml](../.github/workflows/ci-cd.yml) runs lint, unit tests, MySQL migrations, a Compose smoke test, and GHCR publishing. SSH deployment is opt-in.
- Production configuration is in [../docker-compose.prod.yml](../docker-compose.prod.yml); configure its required secrets on the host and GitHub Actions.
