# Business Rules

- Enrollment count never exceeds capacity. Backend performs atomic conditional update and transaction; frontend never increments/decrements seats locally.
- One student registers at most once per section and at most one section per subject per semester.
- A student's registered section schedules cannot overlap.
- A room or lecturer cannot have overlapping sections for the same day, periods, and weeks.
- Cancellation deletes the registration and decrements count in one backend transaction; students can only cancel their own registrations.
- Lecturers only access sections they teach. ADMIN manages subjects/sections and can view rosters.
- A subject with sections cannot be deleted; a section with registrations cannot be deleted.
- `GET /api/sections` returns `remainingSeats`, `full`, and `registeredByMe`; these drive UI state but backend remains authoritative under concurrent requests.
- Frontend refreshes relevant server data after every successful write.