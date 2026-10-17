# Traceability

| Source requirement/use case | API contract | Frontend route | Test status |
|---|---|---|---|
| UC001 Login/RBAC | `POST /auth/login`, `GET /auth/me` | `/login`, role routes | Login UI and role guard implemented; backend schema/integration unverified. |
| UC002 Manage subjects/sections | `/subjects`, `/sections`, `/sections/lookups` | `/admin/subjects`, `/admin/sections` | Read-only subject/section lists implemented; CRUD writes await OpenAPI. |
| UC003 Admin class roster | `GET /sections/{id}/students` | `/app/sections/:sectionId/students` | Roster count view implemented; student field list awaits OpenAPI. |
| UC004 Student session/ownership | JWT, `/me` APIs | Student route guard | Client guard exists; backend authorization not tested. |
| UC005 Register | `GET /sections`, `POST /registrations`, `GET /registrations/me` | `/app/sections` | Implemented; browser mock smoke verified register, refetch, and `registeredByMe`. |
| UC006 Cancel/change | `DELETE /registrations/{id}`; no atomic change endpoint specified | `/app/registrations` | Cancel implemented and mock smoke verified; change semantics/API remain open. |
| UC007 Student timetable | `/semesters/current`, `/students/me/timetable` | `/app/timetable` | Weekly grid implemented and rendered with mock on mobile; backend schema unverified. |
| UC008 Lecturer timetable | `/semesters/current`, `/lecturers/me/timetable`, `/lecturers/me/sections` | `/app/timetable`, `/app/sections` | Shared weekly grid and lecturer section list implemented; backend integration unverified. |
| UC009 Lecturer roster | `/lecturers/me/sections`, `/sections/{id}/students` | `/app/sections/:sectionId/students` | Roster count view implemented; student field list awaits OpenAPI. |

Paths above are the proposed frontend routes from `frontend-plan.md`; API paths are relative to `/api`. Update this table as features and tests are delivered.