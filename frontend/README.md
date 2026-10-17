# QLDT Frontend

React + TypeScript + Vite app. Implemented slices include the login/auth shell, student section registration/cancellation, weekly timetable, read-only ADMIN catalogs, and lecturer section/roster views.

## Run locally

```bash
npm install
npm run dev
```

Set `VITE_API_BASE_URL` in `.env.local` if the backend is not served from the same origin. The default is `/api`.

## Structure

- `src/app`: router and application layout.
- `src/modules`: auth, catalog, registration, and timetable features.
- `src/shared`: API client and shared UI/hooks/utilities.
- `src/mocks`: reserved for contract-generated mocks.

## Contract note

The login adapter posts `{ "username": "...", "password": "..." }` to `/api/auth/login`, stores `accessToken`, and reads the nested `user` returned by login or `/api/auth/me`. Confirm the exact response/error schema against `../contracts/openapi.yaml` before production integration. ADMIN write operations and roster field rendering remain gated on their missing schemas.