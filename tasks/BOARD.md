# Work Board

| Area / UC | Owner | Status | Dependency |
|---|---|---|---|
| FE shell / UC001 | Frontend | UI and adapter align with FastAPI `accessToken` / nested `user`; mock/browser checks passed | Verify against reviewed OpenAPI and real MySQL |
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
