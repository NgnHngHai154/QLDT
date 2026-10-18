# Task UC005: Student Registration

- Owner: Frontend
- Status: Frontend implemented; browser mock smoke passed; backend registration service currently returns `501 NOT_IMPLEMENTED`
- Requirement: UC005, `docs/business-rules.md`, `docs/api-conventions.md`
- APIs: `GET /api/sections?semesterId=...`, `POST /api/registrations` with `{ "sectionId": ... }`, `GET /api/registrations/me?semesterId=...`
- UI acceptance: show `remainingSeats`, `full`, `registeredByMe`; disable registration when full/already registered; send one registration request; refetch server state after success; map registration conflict errors.
- Tests: browser mock verified section rendering, register confirmation, success response, refetch, and `registeredByMe` badge. This does not verify backend registration behavior: `RegistrationService` is still a scaffold. Full/registered disable states and each documented 409 code still need automated regression tests.
- Blocker: detailed section/registration response schemas and `details[]` shape require `contracts/openapi.yaml`.