# Open Questions

| Topic | Current reading | Status/decision needed |
|---|---|---|
| Account creation | Supplied SRS says accounts are preloaded; no self-registration or account-management use case. | Resolved for frontend: do not build sign-up/account CRUD. Confirm if admin account management is added later. |
| Period-to-time conversion | Timetables use periods 1-12, but no official period clock table was supplied. | Open: show period numbers until the academic schedule is provided. |
| Pagination | Subjects and sections use `page`, `size`, `sort`; roster pagination was not specified. | Partially resolved: paginate subjects/sections; confirm roster behavior from OpenAPI. |

Additional FE integration blockers: add `contracts/openapi.yaml`; confirm login response/`/auth/me` shape, details schema, atomic change-class UX, and timetable period boundary semantics.