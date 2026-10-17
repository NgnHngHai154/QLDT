# Frontend Rules

- Stack: React, TypeScript, Vite, Ant Design, React Router, Axios, TanStack Query.
- Feature code belongs in `src/modules/{auth,catalog,registration,timetable}`. App routing/layout belongs in `src/app`; reusable API/UI/hooks/utils belong in `src/shared`.
- The API client base URL defaults to `/api`. Keep endpoint paths relative to that base.
- Do not guess API fields. `src/shared/api/client.ts` currently contains a provisional login adapter; compare it with `contracts/openapi.yaml` before backend integration.
- Parse API failures using `error`, not `message`. Map `VALIDATION_ERROR` details to fields.
- Never calculate or optimistically mutate enrollment counts. Refetch after successful writes.
- 401 clears session; 403 does not log out. Route visibility is UX only; the server enforces RBAC.
- Run `npm run build` before handing off. Add focused tests with the module implementation.