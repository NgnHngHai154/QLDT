# Work Board

| Area / UC | Owner | Status | Dependency |
|---|---|---|---|
| FE shell / UC001 | Frontend | UI and adapter align with FastAPI `accessToken` / nested `user`; mock/browser checks passed | Verify against reviewed OpenAPI and real MySQL |
| FE UC002 | Frontend | Read-only catalog UI done; backend subject/section services implemented and ready | CRUD UI integration |
| FE UC003/UC009 | Frontend | Roster count UI; backend roster service implemented and verified | Roster student table UI integration |
| FE UC005 | Frontend | Registration UI ready; backend registration service implemented with atomic capacity check | Integration verification |
| FE UC006 | Frontend | Cancel UI ready; backend cancel service implemented with capacity decrement | Integration verification |
| FE UC007/UC008 | Frontend | Weekly grid ready; backend timetable service implemented for student & lecturer | Integration verification |
| BE Auth / UC001 | Backend | FastAPI auth implemented; tests pass | Completed |
| BE catalog/registration/timetable | Backend | All services implemented (UC002, UC003, UC005, UC006, UC007, UC008, UC009); 16/16 tests pass | Completed |
| API/OpenAPI | Backend | `contracts/openapi.yaml` and `contracts/api-types.ts` published and synced with frontend | Completed |
| Database seed | Database | SQL seed verified and loaded against local MySQL | Completed |
| Backend CI/CD / Gateway | DevOps | Workflow, Compose, gateway, and Dependabot integrated; Ruff/tests pass | Completed |
| Playwright E2E | Test owner | Not started | Stable FE and API/mock contract |

Current verification: backend pytest: 16 passed; `ruff check .`, `ruff format --check .`, Alembic `upgrade head` + `check` pass. Contracts openapi.yaml and api-types.ts are fully synced.
