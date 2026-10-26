# Task UC005: Student Registration

- Owner: Frontend
- Status: Registration flow implemented in backend and credit-limit errors handled in FE; browser mock smoke previously passed
- Requirement: UC005, `docs/business-rules.md`, `docs/api-conventions.md`
- APIs: `GET /api/sections?semesterId=...`, `POST /api/registrations` with `{ "sectionId": ... }`, `GET /api/registrations/me?semesterId=...`
- UI acceptance: show `remainingSeats`, `full`, `registeredByMe`; disable registration when full/already registered; send one registration request; refetch server state after success; map registration conflict errors.
- Tests: backend `ruff check .`, `ruff format --check .`, and pytest: 30 passed on SQLite in-memory, including success, duplicates, subject/schedule conflicts, full sections, credit boundary/error, and enrollment invariants. MySQL locking/concurrency remains unverified. Browser mock checks were previously run; the FE-BE `id`/`registrationId` discrepancy remains unresolved pending OpenAPI.
- Blocker: detailed section/registration response schemas and `details[]` shape require `contracts/openapi.yaml`.