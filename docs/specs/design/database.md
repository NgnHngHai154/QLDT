# Database Design Summary

The current SQL source has been moved to `db/schema.sql` and `db/seed/seed.sql` without changing its contents. See `db/README.md` for setup instructions.

Tables: `USERS`, `STUDENTS`, `LECTURERS`, `SUBJECTS`, `SEMESTERS`, `ROOMS`, `COURSE_SECTIONS`, `REGISTRATIONS`. All foreign keys use `ON DELETE RESTRICT`. Exact API field mapping belongs in `docs/naming-map.md` and must be verified against `contracts/openapi.yaml`.

## Verified schema constraints

- Account role is `ADMIN`, `LECTURER`, or `STUDENT`; status is `ACTIVE` or `LOCKED`.
- Student/lecturer/subject/semester/room/section codes are unique within their tables.
- Semester end date follows start date; number of weeks is positive. Subject credits, room capacity, and section max capacity are positive.
- `day_of_week` is 2-8; periods are 1-12; end period is not earlier than start. Start week is at least 1 and end week is not earlier than start.
- Current enrollment is between zero and max capacity. `(student_id, section_id)` registration is unique.
- Schema alone does not enforce schedule overlap, one section per subject/semester, or all ownership policies; backend business rules remain authoritative.

Sample data currently identifies semester `2026.1` as current (`semester_id = 3`), with 100 subjects, 30 rooms, 400 sections, and 11,983 registrations.