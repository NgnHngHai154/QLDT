# ADR 001: Frontend Stack

- Status: Accepted for the initial frontend slice; revisit with the group if required.
- Context: The repository had no frontend scaffold. Five students need to work by feature module and integrate with a REST/JSON backend.
- Decision: Use React + TypeScript + Vite, React Router, Ant Design, Axios, and TanStack Query.
- Rationale: Familiar component ecosystem, fast development server, static typing, role-aware routing, and query invalidation/refetch for server-owned registration state.
- Consequences: Keep generated API types aligned with `contracts/openapi.yaml`. Avoid extra global state until a real need appears. Current login request/response typing remains provisional until the contract is added.