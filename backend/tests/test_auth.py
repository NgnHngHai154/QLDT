import re
from pathlib import Path
from uuid import uuid4

import bcrypt
import pytest
from sanic.response import json

from qldt.app import create_app
from qldt.config import Settings
from qldt.security.rbac import require_roles

ROOT = Path(__file__).resolve().parents[2]
SEED_PATH = ROOT / "db" / "seed" / "seed.sql"


def admin_hash_from_seed() -> str:
    seed = SEED_PATH.read_text(encoding="utf-8")
    match = re.search(r"\(1, 'admin', '([^']+)'", seed)
    assert match, "The canonical seed must define user_id=1 username=admin."
    return match.group(1)


def student_hash_from_seed() -> str:
    seed = SEED_PATH.read_text(encoding="utf-8")
    match = re.search(r"\(13, 'sv20210001', '([^']+)'", seed)
    assert match, "The canonical seed must define student sv20210001 with user_id=13."
    return match.group(1)


class FakeUserRepository:
    def __init__(self, users):
        self.users = users

    async def find_by_username(self, username):
        return next((user for user in self.users if user["username"] == username), None)

    async def find_by_id(self, user_id):
        return next((user for user in self.users if user["user_id"] == user_id), None)


@pytest.fixture
def app():
    password_hash = admin_hash_from_seed()
    users = [
        {
            "user_id": 1,
            "username": "admin",
            "password_hash": password_hash,
            "full_name": "Nguyễn Văn Quản",
            "email": "admin@sis.hust.vn",
            "role": "ADMIN",
            "status": "ACTIVE",
        },
        {
            "user_id": 99,
            "username": "locked-test-user",
            "password_hash": password_hash,
            "full_name": "Locked test account",
            "email": None,
            "role": "STUDENT",
            "status": "LOCKED",
        },
        {
            "user_id": 13,
            "username": "sv20210001",
            "password_hash": student_hash_from_seed(),
            "full_name": "Võ Hoài Hải",
            "email": "sv20210001@sis.hust.vn",
            "role": "STUDENT",
            "status": "ACTIVE",
        },
    ]
    application = create_app(
        settings=Settings(jwt_secret_key="test-secret-key-long-enough-for-hs256"),
        user_repository=FakeUserRepository(users),
        name=f"qldt-auth-test-{uuid4().hex}",
    )

    @application.get("/api/admin/test")
    @require_roles("ADMIN")
    async def admin_test_route(request):
        return json({"ok": True})

    return application


@pytest.mark.asyncio
async def test_seed_contains_one_admin_and_hash_matches_documented_password():
    seed = SEED_PATH.read_text(encoding="utf-8")
    assert len(re.findall(r"\(\d+, '[^']+', '[^']+', '[^']+', '[^']*', 'ADMIN',", seed)) == 1
    assert "'admin02'" not in seed
    assert bcrypt.checkpw(b"admin", admin_hash_from_seed().encode("utf-8"))


@pytest.mark.asyncio
async def test_login_returns_access_token_without_refresh_token(app):
    _, response = await app.asgi_client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin"},
    )

    assert response.status == 200
    assert response.json["status"] == 200
    assert response.json["tokenType"] == "Bearer"
    assert response.json["expiresIn"] == 3600
    assert response.json["user"] == {
        "userId": 1,
        "username": "admin",
        "fullName": "Nguyễn Văn Quản",
        "email": "admin@sis.hust.vn",
        "role": "ADMIN",
    }
    assert "accessToken" in response.json
    assert "refreshToken" not in response.json
    assert "password_hash" not in response.json


@pytest.mark.asyncio
async def test_login_validation_uses_standard_error_envelope(app):
    _, response = await app.asgi_client.post("/api/auth/login", json={"username": "admin"})

    assert response.status == 400
    assert response.json["error"] == "VALIDATION_ERROR"
    assert response.json["details"][0]["field"] == "password"
    assert response.json["path"] == "/api/auth/login"
    assert response.json["timestamp"].endswith("+07:00")


@pytest.mark.asyncio
async def test_invalid_credentials_and_locked_account_have_documented_codes(app):
    _, invalid = await app.asgi_client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "wrong"},
    )
    _, locked = await app.asgi_client.post(
        "/api/auth/login",
        json={"username": "locked-test-user", "password": "admin"},
    )

    assert (invalid.status, invalid.json["error"]) == (401, "INVALID_CREDENTIALS")
    assert (locked.status, locked.json["error"]) == (403, "ACCOUNT_LOCKED")


@pytest.mark.asyncio
async def test_me_returns_camel_case_user_and_requires_bearer_token(app):
    _, login = await app.asgi_client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin"},
    )
    _, me = await app.asgi_client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {login.json['accessToken']}"},
    )
    _, anonymous = await app.asgi_client.get("/api/auth/me")

    assert me.status == 200
    assert me.json["user"]["userId"] == 1
    assert me.json["user"]["fullName"] == "Nguyễn Văn Quản"
    assert anonymous.status == 401
    assert anonymous.json["error"] == "UNAUTHORIZED"


@pytest.mark.asyncio
async def test_rbac_denies_non_admin_and_allows_admin(app):
    _, login = await app.asgi_client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin"},
    )
    _, allowed = await app.asgi_client.get(
        "/api/admin/test",
        headers={"Authorization": f"Bearer {login.json['accessToken']}"},
    )

    assert allowed.status == 200

    _, student_login = await app.asgi_client.post(
        "/api/auth/login",
        json={"username": "sv20210001", "password": "123456"},
    )
    _, denied = await app.asgi_client.get(
        "/api/admin/test",
        headers={"Authorization": f"Bearer {student_login.json['accessToken']}"},
    )
    assert denied.status == 403
    assert denied.json["error"] == "FORBIDDEN"


@pytest.mark.asyncio
async def test_refresh_token_endpoint_is_not_exposed(app):
    _, response = await app.asgi_client.post("/api/auth/refresh")

    assert response.status == 404
    assert response.json["error"] == "NOT_FOUND"