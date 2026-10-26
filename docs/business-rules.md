# Business Rules

- Enrollment count never exceeds capacity. Backend performs atomic conditional update and transaction; frontend never increments/decrements seats locally.
- One student registers at most once per section and at most one section per subject per semester.
- A student's registered section schedules cannot overlap.
- Total credits per semester equal the sum of `SUBJECTS.credits` for the student's registered sections. The system-wide minimum and maximum are configured by `MIN_CREDITS_PER_SEMESTER` and `MAX_CREDITS_PER_SEMESTER` (defaults 12 and 24); the maximum must be at least 1 and no lower than the minimum.
- Registration is rejected when it would exceed the semester maximum. Cancellation is rejected only when the student currently meets the minimum and cancellation would take the total below it; students currently below the minimum may cancel.
- Prerequisite and co-requisite subject rules are out of scope. The schema has no grades table, and the team decided not to implement these checks.
- A room or lecturer cannot have overlapping sections for the same day, periods, and weeks.
- Cancellation deletes the registration and decrements count in one backend transaction; students can only cancel their own registrations.
- Lecturers only access sections they teach. ADMIN manages subjects/sections and can view rosters.
- A subject with sections cannot be deleted; a section with registrations cannot be deleted.
- `GET /api/sections` returns `remainingSeats`, `full`, and `registeredByMe`; these drive UI state but backend remains authoritative under concurrent requests.
- Frontend refreshes relevant server data after every successful write.