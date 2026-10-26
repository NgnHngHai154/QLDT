# Work Board

| Area / UC | Owner | Status | Dependency |
|---|---|---|---|
| FE shell / UC001 | Frontend | UI and adapter align with FastAPI `accessToken` / nested `user`; mock/browser checks passed | Verify against reviewed OpenAPI and real MySQL |
| FE UC002 | Frontend | Read-only catalog UI done; backend subject/section service returns 501; CRUD UI pending | Implement backend services; OpenAPI write schemas and validation details |
| FE UC003/UC009 | Frontend | Roster count UI; backend roster service returns 501 and detail fields are pending | Implement roster service; OpenAPI schema and pagination |
| FE UC005 | Frontend | Registration UI handles `CREDIT_LIMIT_EXCEEDED`; backend registration flow and credit maximum implemented; backend tests pass on SQLite | Reconcile `id`/`sectionId`/`semesterId` naming with reviewed OpenAPI; verify MySQL |
| FE UC006 | Frontend | Cancel UI handles `CREDIT_LIMIT_BELOW_MIN`; backend cancellation and credit minimum implemented; backend tests pass on SQLite | Reconcile FE-BE field naming; decide change-class atomic API/UX; verify MySQL |
| FE UC007/UC008 | Frontend | Weekly grid and mock render passed; backend timetable service returns 501 | Implement timetable service; verify response/period boundaries |
| BE Auth / UC001 | Backend | FastAPI auth implemented; 13 tests pass with SQLite fixtures | Verify against reviewed OpenAPI and real MySQL |
| BE catalog/registration/timetable | Backend | Registration register/cancel/list implemented with transaction rules, row locking, and credit limits; catalog and timetable service operations remain `501 NOT_IMPLEMENTED` | MySQL integration/concurrency verification; implement remaining catalog/timetable services |
| API/OpenAPI | Backend | Generated FastAPI docs available at `/api/openapi.json`; reviewed contract not supplied | Publish `contracts/openapi.yaml`; reconcile schemas |
| Database seed | Database | SQL seed is canonical under `db/seed/`; backend script provides matching minimal dev accounts | Verify seed load against local MySQL |
| Backend CI/CD / Gateway | DevOps | Workflow, Compose, gateway, and Dependabot integrated; Ruff/tests/SQLite migration parity pass | Run Docker/MySQL integration and configure optional deployment secrets |
| Playwright E2E | Test owner | Not started | Stable FE and API/mock contract |

Current verification: backend pytest: 30 passed on SQLite in-memory; `ruff check .` and `ruff format --check .` pass; frontend `npm run build` passes (Vite reports a large JS chunk warning). Docker Compose image build/startup, MySQL `alembic upgrade head` + `alembic check`, and all Gateway smoke checks pass. Registration business rules and concurrent `SELECT ... FOR UPDATE` behavior remain unverified on MySQL. The OpenAPI contract is still pending, and FE currently reads `registrationId`/`sectionId`/`semesterId` while backend DTOs expose `id`.