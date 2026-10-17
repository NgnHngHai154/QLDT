# Sanic Backend

Python/Sanic backend using the `src/qldt` package layout. Authentication reads `USERS` from MySQL; there is no production mock-user fallback. The seed currently defines one ADMIN, `admin` / `admin`, and lecturer/student accounts use `123456`.

## Local run

Python 3.11 or newer and MySQL 8.0.16+ are required.

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pip install -e .
$env:JWT_SECRET_KEY = (python -c "import secrets; print(secrets.token_urlsafe(48))")
$env:DB_HOST = "localhost"
$env:DB_NAME = "qldt"
$env:DB_USER = "root"
$env:DB_PASSWORD = "your-local-password"
python run.py
```

`JWT_SECRET_KEY` is required and must be at least 32 bytes. No secret is shipped as a default.

## Auth endpoints

- `POST /api/auth/login`: username/password; responds with `accessToken`, `expiresIn`, and camelCase user data.
- `GET /api/auth/me`: requires `Authorization: Bearer <accessToken>`.
- Access token lifetime is 3600 seconds. There is no refresh-token endpoint, matching the SRS.

Run tests with `pytest` from this directory. API schema details should be reconciled with `../contracts/openapi.yaml` when that contract is published.