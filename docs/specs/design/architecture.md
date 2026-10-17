# System Architecture Summary

This is a summary of the architecture supplied in the SRS, not a replacement for detailed design diagrams.

- Three tiers: responsive browser client, REST/JSON server, relational database.
- Backend layers: View -> Controller -> Service -> Repository -> Entity.
- Backend modules: auth, catalog, registration, timetable; shared security package includes JWT filter, role checker, and password encoder.
- Cross-cutting authorization: endpoint role check plus service-level ownership check.
- Frontend consumes `/api` and must follow `docs/api-conventions.md`; the final machine-readable API contract is `contracts/openapi.yaml` when provided.

Detailed class/sequence diagrams and deployment decisions belong to their respective owners.

## UI reference

The public HUST portal groups services by audience and links student services such as timetables and study registration. Use this only as inspiration for role-based navigation and academic identity. The authenticated registration workflow was not available for inspection and must follow this project's SRS/API contract instead.