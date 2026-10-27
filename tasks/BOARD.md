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
| FE UC002 | Frontend | Read-only catalog UI done; backend subject/section services implemented and ready | CRUD UI integration |
| FE UC003/UC009 | Frontend | Roster count UI; backend roster service implemented and verified | Roster student table UI integration |
| FE UC005 | Frontend | Registration UI handles `CREDIT_LIMIT_EXCEEDED`; backend enforces capacity, schedule, duplicate, and maximum-credit rules with per-student row locking | Integration verification |
| FE UC006 | Frontend | Cancel UI handles `CREDIT_LIMIT_BELOW_MIN`; backend enforces ownership/minimum-credit rules and decrements capacity | Integration verification; atomic change-class behavior remains unspecified |
| FE UC007/UC008 | Frontend | Weekly grid ready; backend timetable service implemented for student & lecturer | Integration verification |
| BE Auth / UC001 | Backend | FastAPI auth implemented; tests pass | Completed |
| BE catalog/registration/timetable | Backend | Services implemented for UC002-UC009; registration includes credit limits, row locking, and atomic capacity updates | Verify the merged implementation with backend checks |
| API/OpenAPI | Backend | `contracts/openapi.yaml` and `contracts/api-types.ts` published and synced with frontend | Completed |
| Database seed | Database | SQL seed verified and loaded against local MySQL | Completed |
| Backend CI/CD / Gateway | DevOps | Workflow, Compose, gateway, and Dependabot integrated; Ruff/tests pass | Completed |
| Playwright E2E | Test owner | Not started | Stable FE and API/mock contract |

Current verification from the latest integration: run the backend checks in `backend/CLAUDE.md` before merging. MySQL row-locking/concurrency and full frontend-to-API integration should be verified in the target environment.
