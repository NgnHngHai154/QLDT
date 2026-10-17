# Work Board

| Area / UC | Owner | Status | Dependency |
|---|---|---|---|
| FE shell / UC001 | Frontend | UI done; backend integration pending | OpenAPI login and `/auth/me` schemas |
| FE UC002 | Frontend | Read-only catalog done; CRUD pending | OpenAPI write schemas, validation details, delete error mapping |
| FE UC003/UC009 | Frontend | Roster count view; detail fields pending | OpenAPI roster item schema and pagination |
| FE UC005 | Frontend | Implemented; browser mock smoke passed | Verify request/response against OpenAPI/backend |
| FE UC006 | Frontend | Cancel flow implemented; mock smoke passed | Change-class atomic API/UX decision |
| FE UC007/UC008 | Frontend | Weekly grid implemented; student mock render passed | Verify timetable response/period boundaries with OpenAPI/backend |
| BE Auth / UC001 | Backend | Sanic implementation done; 7 tests pass | Verify against OpenAPI and real MySQL |
| API/OpenAPI | Backend | Not started | Publish `contracts/openapi.yaml` |
| Database seed | Database | New one-admin seed is canonical under `db/seed/` | Verify seed load against local MySQL |
| Playwright E2E | Test owner | Not started | Stable FE and API/mock contract |

Current verification: frontend `npm run build` passes; Sanic auth suite: 7 passed. Browser checks: login on 390px without horizontal overflow; role guard denies an ADMIN route for STUDENT without clearing the token; UC005 register/refetch and UC006 cancel/refetch pass with mocks; timetable renders at 390px. MySQL and OpenAPI integration remain unverified.