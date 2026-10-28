# Database Workspace

Database source is organized here:

- `schema.sql`: relational schema.
- `seed/seed.sql`: sample accounts and academic data.
- `../backend/migrations/`: Alembic migrations used by the API and CI; keep them aligned with this canonical SQL schema.

Requires MySQL 8.0.16 or later. These SQL files are the canonical full sample database path.
On a new, empty database, load the schema and then the seed:

```bash
mysql -u root -p < schema.sql
mysql -u root -p < seed/seed.sql
```

For an API-managed database, create the `qldt` database and run `alembic upgrade head`
from `backend/` instead. Do not load `schema.sql` and apply the initial Alembic migration
to the same empty database; they are alternate ways to create the same schema.

For routine local application development, follow the root [README](../README.md): migrations
create the schema and `python -m scripts.seed` inserts the small idempotent dev fixture. Do not
run that dev seed and the full SQL seed against the same database. Neither seed command is a
database reset or a repair command; inspect/back up existing data before changing or reloading it.

## Sample accounts and data

The seed now has exactly one ADMIN. Its password is `admin`; lecturer and student accounts use `123456`.

| Role | Username | Password | Role-specific ID |
|---|---|---|---|
| ADMIN | `admin` | `admin` | None |
| LECTURER | `gv001` through `gv010` | `123456` | `GV001` through `GV010` |
| STUDENT | `sv20210001` through `sv20211000` | `123456` | `20210001` through `20211000` |

The seed contains 1 admin, 10 lecturers, 1,000 students, 100 subjects, 1 active semester (`2026.1`, `semester_id = 1`), 30 rooms, and 400 sections in this single active registration semester. Registrations start empty and `current_enrollment` starts at 0. Student usernames use `sv` followed by student code.

Do not expose password hashes to the client.
