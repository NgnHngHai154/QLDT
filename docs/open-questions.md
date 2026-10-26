# Open Questions

| Topic | Current reading | Status/decision needed |
|---|---|---|
| Account creation | Supplied SRS says accounts are preloaded; no self-registration or account-management use case. | Resolved for frontend: do not build sign-up/account CRUD. Confirm if admin account management is added later. |
| Period-to-time conversion | Timetables use periods 1-12, but no official period clock table was supplied. | Open: show period numbers until the academic schedule is provided. |
| Pagination | Subjects and sections use `page`, `size`, `sort`; roster pagination was not specified. | Partially resolved: paginate subjects/sections; confirm roster behavior from OpenAPI. |
| Semester credit limits | The implementation defaults to minimum 12 and maximum 24 credits, configurable system-wide with environment variables. | Temporary values only; the group must confirm the actual minimum and maximum. |
| Prerequisite/co-requisite subjects | Not checked. The schema has no grades table. | Team decision: keep both rules out of scope. Revisit only if the scope/schema changes. |

Additional FE integration blockers: add `contracts/openapi.yaml`; confirm login response/`/auth/me` shape, details schema, atomic change-class UX, and timetable period boundary semantics.

FE-BE field-name differences observed while implementing registration: backend DTOs expose `id` for registrations, sections, and semesters, while the frontend pages currently read `registrationId`, `sectionId`, and `semesterId`. The contract is not yet available, so the implementation does not rename these fields; reconcile the DTOs and FE adapters against the reviewed OpenAPI contract before end-to-end integration.