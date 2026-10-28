# QLDT Frontend

React + TypeScript + Vite app. Implemented slices include the login/auth shell, student section registration/cancellation, weekly timetable, unified course and section catalogs, and lecturer section/roster views.

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

## Key Features

- Single active registration semester: registration, timetable, and section views auto-bind to the active semester. Course catalog reads the backend subject API; admin subject/section forms and timetable assignments persist through backend APIs.
- Roster student table is implemented in `SectionRosterPage` for UC003/UC009.
- Error handling maps API error codes directly to user feedback.

## UI conventions

- Shared typography and layout tokens live in `src/styles.css`; keep font stacks, spacing, cards, tables, and form controls consistent across modules.
- The academic portal uses a restrained HUST-inspired red accent and table-first information hierarchy. Avoid module-local font overrides unless a content type needs a deliberate distinction.
