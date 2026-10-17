# Naming Map: Database to JSON

This is a partial map based only on the supplied conventions and SRS summary. It is not a replacement for the FE-BE section 3.2 or `contracts/openapi.yaml`. Do not generate client models from guessed mappings.

| Database field | JSON/API name known from supplied summary | Status |
|---|---|---|
| `USERS.user_id` | `userId` | Named in JWT claim summary; `/auth/me` response shape still needs OpenAPI. |
| `USERS.role` | `role` | Confirmed enum values `ADMIN`, `LECTURER`, `STUDENT`. |
| `COURSE_SECTIONS.section_id` | `sectionId` | FK/body naming convention; verify entity response schema. |
| `COURSE_SECTIONS.subject_id` | `subjectId` on writes; `subject: {...}` on reads | Object's inner schema needs OpenAPI. |
| `COURSE_SECTIONS.current_enrollment` | `currentEnrollment` | Named by the supplied business-rule summary. |
| `COURSE_SECTIONS.max_capacity` | `maxCapacity` | Named by the supplied business-rule summary. |
| Schedule fields | `dayOfWeek`, `startPeriod`, `endPeriod`, `date`, `week` | Named in timetable requirements; complete object schema needs OpenAPI. |
| Computed section fields | `remainingSeats`, `full`, `registeredByMe` | Explicitly named for `GET /sections`; not DB columns. |

All other field mappings, nullability, nested objects and pagination metadata are pending the original naming-map section/OpenAPI.