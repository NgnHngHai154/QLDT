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

- Single active registration semester: registration, timetable, and section views auto-bind to the active semester; course catalog is unified without semester fragmentation or prerequisite/corequisite constraints.
- Roster student table is implemented in `SectionRosterPage` for UC003/UC009.
- Error handling maps API error codes directly to user feedback.
