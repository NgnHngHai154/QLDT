# Traceability

| Source requirement/use case | API contract | Frontend route | Test status |
|---|---|---|---|
| UC001 Login/RBAC | `POST /auth/login`, `GET /auth/me` | `/login`, role routes | Login UI and role guard implemented; FastAPI auth tests pass with SQLite fixtures; verify against MySQL/OpenAPI. |
| UC002 Manage subjects/sections | `/subjects`, `/sections`, `/sections/lookups` | `/admin/subjects`, `/admin/sections` | Read-only UI exists; backend subject/section services currently return `501 NOT_IMPLEMENTED`; CRUD writes await OpenAPI. |
| UC003 Admin class roster | `GET /sections/{id}/students` | `/app/sections/:sectionId/students` | Roster count UI exists; backend roster service currently returns `501 NOT_IMPLEMENTED`; student field list awaits OpenAPI. |
| UC004 Student session/ownership | JWT, `/me` APIs | Student route guard | Client guard exists; backend authorization not tested. |
| UC005 Register | `GET /sections`, `POST /registrations`, `GET /registrations/me` | `/app/sections` | FE mock smoke verified register/refetch; backend registration service currently returns `501 NOT_IMPLEMENTED`. |
| UC006 Cancel/change | `DELETE /registrations/{id}`; no atomic change endpoint specified | `/app/registrations` | FE cancel mock smoke passed; backend registration service currently returns `501 NOT_IMPLEMENTED`; change semantics/API remain open. |
| UC007 Student timetable | `/semesters/current`, `/students/me/timetable` | `/app/timetable` | Weekly grid rendered with mock on mobile; backend timetable service currently returns `501 NOT_IMPLEMENTED`. |
| UC008 Lecturer timetable | `/semesters/current`, `/lecturers/me/timetable`, `/lecturers/me/sections` | `/app/timetable`, `/app/sections` | Shared weekly grid and lecturer section UI exist; backend timetable service currently returns `501 NOT_IMPLEMENTED`. |
| UC009 Lecturer roster | `/lecturers/me/sections`, `/sections/{id}/students` | `/app/sections/:sectionId/students` | Roster count UI exists; backend roster service currently returns `501 NOT_IMPLEMENTED`; student field list awaits OpenAPI. |

Frontend paths reflect the current app routes; API paths are relative to `/api`. Update this table as features and tests are delivered.