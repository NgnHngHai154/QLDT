# Traceability

| Source requirement/use case | API contract | Frontend route | Test status |
|---|---|---|---|
| UC001 Login/RBAC | `POST /auth/login`, `GET /auth/me` | `/login`, role routes | Implemented; auth and RBAC tests pass with SQLite fixtures; verified against local MySQL and OpenAPI. |
| UC002 Manage subjects/sections | `/subjects`, `/sections`, `/sections/lookups` | `/admin/subjects`, `/admin/sections` | Backend services and CRUD endpoints implemented; conflict checks verified with automated tests. |
| UC003 Admin class roster | `GET /sections/{id}/students` | `/app/sections/:sectionId/students` | Backend roster service implemented and verified with automated tests. |
| UC004 Student session/ownership | JWT, `/me` APIs | Student route guard | Implemented; token authentication and data ownership enforced at service layer. |
| UC005 Register | `GET /sections`, `POST /registrations`, `GET /registrations/me` | `/app/sections` | Backend registration service implemented with atomic capacity check and conflict validation; verified via tests. |
| UC006 Cancel/change | `DELETE /registrations/{id}` | `/app/registrations` | Backend cancel service implemented with atomic capacity decrement; verified via tests. |
| UC007 Student timetable | `/semesters/current`, `/students/me/timetable` | `/app/timetable` | Backend timetable service implemented with weekly date calculations; verified via tests. |
| UC008 Lecturer timetable | `/semesters/current`, `/lecturers/me/timetable`, `/lecturers/me/sections` | `/app/timetable`, `/app/sections` | Backend timetable and lecturer section service implemented; verified via tests. |
| UC009 Lecturer roster | `/lecturers/me/sections`, `/sections/{id}/students` | `/app/sections/:sectionId/students` | Backend roster service with lecturer ownership check implemented; verified via tests. |

Frontend paths reflect the current app routes; API paths are relative to `/api`.
