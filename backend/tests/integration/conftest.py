"""Fixture cho kiểm thử tích hợp FE-BE-DB của Feature 10.

Các test tự bỏ qua khi stack chưa chạy. Địa chỉ và tài khoản có thể ghi đè bằng
biến môi trường QLDT_*; thông tin MySQL được đọc từ file .env ở thư mục gốc repo
(hoặc QLDT_DATABASE_URL) để không phụ thuộc cấu hình SQLite của test đơn vị.
"""

import os
from pathlib import Path

import httpx
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

REPO_ROOT = Path(__file__).resolve().parents[3]


def _read_env_file() -> dict[str, str]:
    values: dict[str, str] = {}
    path = REPO_ROOT / ".env"
    if not path.is_file():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _file_setting(name: str, default: str) -> str:
    return _read_env_file().get(name, default)


def _is_up(url: str, path: str = "/health") -> bool:
    try:
        response = httpx.get(f"{url.rstrip('/')}{path}", timeout=2.0, follow_redirects=True)
    except httpx.HTTPError:
        return False
    return response.is_success


@pytest.fixture(scope="session")
def gateway_url() -> str:
    return os.environ.get("QLDT_GATEWAY_URL", "http://localhost:8080").rstrip("/")


@pytest.fixture(scope="session")
def frontend_url() -> str:
    return os.environ.get("QLDT_FRONTEND_URL", "http://localhost:5173").rstrip("/")


@pytest.fixture(scope="session")
def gateway_client(gateway_url):
    if not _is_up(gateway_url):
        pytest.skip(f"Gateway/backend chưa chạy tại {gateway_url}")
    with httpx.Client(base_url=gateway_url, timeout=10.0) as client:
        yield client


@pytest.fixture(scope="session")
def api(gateway_url):
    if not _is_up(gateway_url, "/api/subjects"):
        pytest.skip(f"API chưa chạy tại {gateway_url}/api")
    with httpx.Client(base_url=f"{gateway_url}/api", timeout=10.0) as client:
        yield client


@pytest.fixture(scope="session")
def frontend_client(frontend_url):
    if not _is_up(frontend_url, "/"):
        pytest.skip(f"Frontend chưa chạy tại {frontend_url}")
    with httpx.Client(base_url=frontend_url, timeout=10.0) as client:
        yield client


@pytest.fixture(scope="session")
def admin_headers(api):
    username = os.environ.get("QLDT_ADMIN_USERNAME", "admin")
    password = os.environ.get("QLDT_ADMIN_PASSWORD", "admin")
    response = api.post("/auth/login", json={"username": username, "password": password})
    if response.status_code != 200:
        pytest.skip(
            f"Không đăng nhập được ADMIN ({response.status_code}); kiểm tra seed và tài khoản"
        )
    return {"Authorization": f"Bearer {response.json()['accessToken']}"}


@pytest.fixture(scope="session")
def db_engine():
    database_url = os.environ.get("QLDT_DATABASE_URL")
    if not database_url:
        database_url = URL.create(
            "mysql+pymysql",
            username=_file_setting("MYSQL_USER", "app"),
            password=_file_setting("MYSQL_PASSWORD", ""),
            host=_file_setting("MYSQL_HOST", "127.0.0.1"),
            port=int(_file_setting("MYSQL_PORT", "3306")),
            database=_file_setting("MYSQL_DATABASE", "qldt"),
            query={"charset": "utf8mb4"},
        ).render_as_string(hide_password=False)

    try:
        engine = create_engine(
            database_url,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 3},
        )
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001 - bỏ qua khi chưa bật MySQL
        pytest.skip(f"Không kết nối được MySQL để đối chiếu: {exc}")

    yield engine
    engine.dispose()
