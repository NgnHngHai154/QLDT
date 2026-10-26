# Work Board

| Area / UC | Owner | Status | Dependency |
|---|---|---|---|
| FE shell / UC001 | Frontend | UI and adapter align with FastAPI `accessToken` / nested `user`; mock/browser checks passed | Verify against reviewed OpenAPI and real MySQL |
| FE UC002 | Frontend | Read-only catalog UI done; backend subject/section service returns 501; CRUD UI pending | Implement backend services; OpenAPI write schemas and validation details |
| FE UC003/UC009 | Frontend | Roster count UI; backend roster service returns 501 and detail fields are pending | Implement roster service; OpenAPI schema and pagination |
| FE UC005 | Frontend | Registration UI and browser mock smoke passed; backend registration service returns 501 | Implement service and verify against OpenAPI/backend |
| FE UC006 | Frontend | Cancel UI and browser mock smoke passed; backend registration service returns 501 | Implement service; change-class atomic API/UX decision |
| FE UC007/UC008 | Frontend | In Progress — weekly grid and Admin schedule/room/lecturer assignment UI implemented with local conflict checks; backend timetable service returns 501 | Implement timetable service; verify response/period boundaries |
| BE Auth / UC001 | Backend | FastAPI auth implemented; 13 tests pass with SQLite fixtures | Verify against reviewed OpenAPI and real MySQL |
| BE catalog/registration/timetable | Backend | Routes, DTOs, repositories, and migration scaffold integrated; service operations return `501 NOT_IMPLEMENTED` | Implement business services and focused tests |
| API/OpenAPI | Backend | Generated FastAPI docs available at `/api/openapi.json`; reviewed contract not supplied | Publish `contracts/openapi.yaml`; reconcile schemas |
| Database seed | Database | SQL seed is canonical under `db/seed/`; backend script provides matching minimal dev accounts | Verify seed load against local MySQL |
| Backend CI/CD / Gateway | DevOps | Workflow, Compose, gateway, and Dependabot integrated; Ruff/tests/SQLite migration parity pass | Run Docker/MySQL integration and configure optional deployment secrets |
| Playwright E2E | Test owner | Not started | Stable FE and API/mock contract |

Current verification: backend pytest: 13 passed; `ruff check .`, `ruff format --check .`, Alembic `upgrade head` + `check` on SQLite, and Compose config validation pass. Frontend `npm run build` and prior browser mock checks remain as previously verified. Docker daemon is unavailable in this environment, so MySQL migration, container startup, and Gateway smoke test remain unverified; OpenAPI contract is still pending.