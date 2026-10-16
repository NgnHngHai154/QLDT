"""
=======================================================================
auth.py  –  Module Xác thực & Phân quyền QLDT
=======================================================================
Chức năng:
  1. Đăng nhập tập trung (SSO-like) qua JWT
     - POST /auth/login      → cấp access_token + refresh_token
     - POST /auth/refresh    → cấp access_token mới từ refresh_token
     - POST /auth/logout     → thu hồi refresh_token (blacklist)
  2. Phân quyền RBAC (Role-Based Access Control)
     - 3 vai trò: ADMIN, LECTURER, STUDENT
     - Decorator @require_roles(...) bảo vệ endpoint
  3. Tích hợp MySQL – đọc bảng USERS theo schema QLDT

Cài thư viện:
  pip install flask flask-jwt-extended bcrypt mysql-connector-python

Chạy thử (chế độ standalone / không cần MySQL thật):
  python auth.py                 # sử dụng IN-MEMORY mock database

Chạy với MySQL thật:
  Đặt biến môi trường DB_* (xem phần config bên dưới)
  python auth.py
=======================================================================
"""

import os
import datetime
import functools
from typing import Optional, Set

# ── Flask & JWT ──────────────────────────────────────────────────────
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

# ── Bcrypt ───────────────────────────────────────────────────────────
import bcrypt

# ── MySQL (tuỳ chọn) ─────────────────────────────────────────────────
try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

# =======================================================================
# CẤU HÌNH
# =======================================================================

class Config:
    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "qldt-super-secret-change-me-in-prod")
    JWT_ACCESS_TOKEN_EXPIRES: int = int(os.getenv("JWT_ACCESS_EXPIRES", 3600))       # 1 giờ
    JWT_REFRESH_TOKEN_EXPIRES: int = int(os.getenv("JWT_REFRESH_EXPIRES", 86400 * 7))  # 7 ngày

    # MySQL
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))
    DB_NAME: str = os.getenv("DB_NAME", "qldt")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

    # Chạy mà không cần MySQL thật?
    USE_MOCK_DB: bool = os.getenv("USE_MOCK_DB", "true").lower() == "true"

    # Flask
    DEBUG: bool = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    PORT: int = int(os.getenv("PORT", 5000))


# =======================================================================
# IN-MEMORY MOCK DATABASE (dùng khi không có MySQL)
# Mật khẩu mặc định: 123456  (bcrypt hash từ seed.sql)
# =======================================================================

_BCRYPT_123456 = "$2a$10$t8KMwxixC78cehNtGWqNKOgCrvdl/N24lai2sQwK9E1HyaQgG0N0K"

MOCK_USERS: dict[str, dict] = {
    "admin": {
        "user_id": 1,
        "username": "admin",
        "password_hash": _BCRYPT_123456,
        "full_name": "Nguyễn Văn Quản",
        "email": "admin@sis.hust.vn",
        "role": "ADMIN",
        "status": "ACTIVE",
    },
    "admin02": {
        "user_id": 2,
        "username": "admin02",
        "password_hash": _BCRYPT_123456,
        "full_name": "Trần Thị Hương",
        "email": "admin02@sis.hust.vn",
        "role": "ADMIN",
        "status": "ACTIVE",
    },
    "gv001": {
        "user_id": 3,
        "username": "gv001",
        "password_hash": _BCRYPT_123456,
        "full_name": "Hứa Tuấn Minh",
        "email": "gv001@sis.hust.vn",
        "role": "LECTURER",
        "status": "ACTIVE",
    },
    "sv20210001": {
        "user_id": 13,
        "username": "sv20210001",
        "password_hash": _BCRYPT_123456,
        "full_name": "Võ Hoài Hải",
        "email": "sv20210001@sis.hust.vn",
        "role": "STUDENT",
        "status": "ACTIVE",
    },
    # Tài khoản bị khoá để test
    "locked_user": {
        "user_id": 999,
        "username": "locked_user",
        "password_hash": _BCRYPT_123456,
        "full_name": "Tài Khoản Bị Khoá",
        "email": "locked@sis.hust.vn",
        "role": "STUDENT",
        "status": "LOCKED",
    },
}


# =======================================================================
# BLACKLIST REFRESH TOKENS (in-memory; production → Redis / DB)
# =======================================================================

_refresh_blacklist: Set[str] = set()


def _blacklist_token(jti: str) -> None:
    _refresh_blacklist.add(jti)


def _is_blacklisted(jti: str) -> bool:
    return jti in _refresh_blacklist


# =======================================================================
# DATA ACCESS LAYER
# =======================================================================

def _get_db_connection():
    """Tạo kết nối MySQL. Trả về None nếu lỗi hoặc không cấu hình."""
    if not MYSQL_AVAILABLE:
        return None
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            charset="utf8mb4",
            collation="utf8mb4_unicode_ci",
        )
        return conn
    except mysql.connector.Error as e:
        print(f"[DB ERROR] {e}")
        return None


def find_user_by_username(username: str) -> Optional[dict]:
    """
    Tra cứu user theo username.
    Ưu tiên MySQL nếu kết nối thành công, fallback về mock DB.
    """
    if not Config.USE_MOCK_DB:
        conn = _get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(
                    "SELECT user_id, username, password_hash, full_name, "
                    "email, role, status FROM USERS WHERE username = %s",
                    (username,),
                )
                row = cursor.fetchone()
                return row
            finally:
                conn.close()
        # Nếu lỗi kết nối → fallback mock
        print("[WARN] MySQL unavailable, falling back to mock DB")

    return MOCK_USERS.get(username)


# =======================================================================
# RBAC – MA TRẬN QUYỀN
# =======================================================================

# Các quyền được định nghĩa theo cặp (resource, action)
PERMISSIONS: dict[str, set] = {
    "ADMIN": {
        # Quản lý người dùng
        "user:read", "user:create", "user:update", "user:delete",
        # Quản lý môn học
        "subject:read", "subject:create", "subject:update", "subject:delete",
        # Quản lý học kỳ
        "semester:read", "semester:create", "semester:update", "semester:delete",
        # Quản lý phòng
        "room:read", "room:create", "room:update", "room:delete",
        # Quản lý lớp học phần
        "section:read", "section:create", "section:update", "section:delete",
        # Quản lý đăng ký
        "registration:read", "registration:create", "registration:delete",
        # Thống kê
        "report:read",
    },
    "LECTURER": {
        # Xem thông tin
        "user:read",
        "subject:read",
        "semester:read",
        "room:read",
        # Lớp học phần của mình
        "section:read",
        # Danh sách SV trong lớp
        "registration:read",
    },
    "STUDENT": {
        # Thông tin cá nhân
        "user:read",
        # Tra cứu
        "subject:read",
        "semester:read",
        "section:read",
        # Đăng ký và huỷ học phần của mình
        "registration:read", "registration:create", "registration:delete",
    },
}


def has_permission(role: str, permission: str) -> bool:
    """Kiểm tra role có quyền `permission` hay không."""
    return permission in PERMISSIONS.get(role, set())


# =======================================================================
# FLASK APPLICATION
# =======================================================================

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(
    seconds=Config.JWT_ACCESS_TOKEN_EXPIRES
)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(
    seconds=Config.JWT_REFRESH_TOKEN_EXPIRES
)
# Vô hiệu hoá JWT trong header Location (tránh redirect bug)
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_TYPE"] = "Bearer"

jwt = JWTManager(app)


# ── Callback kiểm tra blacklist refresh token ────────────────────────
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    return _is_blacklisted(jwt_payload["jti"])


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"code": 401, "message": "Token đã bị thu hồi"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"code": 401, "message": f"Token không hợp lệ: {error}"}), 401


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"code": 401, "message": "Token đã hết hạn"}), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"code": 401, "message": "Thiếu Authorization header"}), 401


# =======================================================================
# DECORATOR RBAC
# =======================================================================

def require_roles(*roles: str):
    """
    Decorator bảo vệ endpoint theo vai trò.
    Dùng sau @jwt_required().

    Ví dụ:
        @app.route("/admin/users")
        @jwt_required()
        @require_roles("ADMIN")
        def list_users(): ...
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role: str = claims.get("role", "")
            if user_role not in roles:
                return jsonify({
                    "code": 403,
                    "message": f"Không có quyền truy cập. Yêu cầu vai trò: {list(roles)}"
                }), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def require_permission(permission: str):
    """
    Decorator kiểm tra quyền cụ thể (dạng 'resource:action').
    Dùng sau @jwt_required().
    Ví dụ:
        @app.route("/subjects", methods=["POST"])
        @jwt_required()
        @require_permission("subject:create")
        def create_subject(): ...
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role: str = claims.get("role", "")
            if not has_permission(role, permission):
                return jsonify({
                    "code": 403,
                    "message": f"Không có quyền '{permission}'"
                }), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


# =======================================================================
# AUTH ENDPOINTS
# =======================================================================

@app.route("/auth/login", methods=["POST"])
def login():
    """
    POST /auth/login
    Body JSON: { "username": "...", "password": "..." }
    Response 200:
    {
        "code": 200,
        "access_token": "<JWT>",
        "refresh_token": "<JWT>",
        "token_type": "Bearer",
        "expires_in": 3600,
        "user": { "user_id", "username", "full_name", "email", "role" }
    }
    """
    data = request.get_json(silent=True) or {}
    username: str = data.get("username", "").strip()
    password: str = data.get("password", "")

    # --- Validate input ---
    if not username or not password:
        return jsonify({"code": 400, "message": "username và password không được để trống"}), 400

    # --- Tra cứu user ---
    user = find_user_by_username(username)
    if not user:
        return jsonify({"code": 401, "message": "Sai tên đăng nhập hoặc mật khẩu"}), 401

    # --- Kiểm tra trạng thái ---
    if user["status"] == "LOCKED":
        return jsonify({"code": 403, "message": "Tài khoản đã bị khoá"}), 403

    # --- Xác thực mật khẩu (bcrypt) ---
    stored_hash: str = user["password_hash"]
    try:
        password_ok = bcrypt.checkpw(
            password.encode("utf-8"),
            stored_hash.encode("utf-8"),
        )
    except Exception:
        password_ok = False

    if not password_ok:
        return jsonify({"code": 401, "message": "Sai tên đăng nhập hoặc mật khẩu"}), 401

    # --- Tạo JWT claims ---
    identity = str(user["user_id"])
    additional_claims = {
        "username": user["username"],
        "full_name": user["full_name"],
        "email": user.get("email"),
        "role": user["role"],
    }

    access_token = create_access_token(
        identity=identity,
        additional_claims=additional_claims,
    )
    refresh_token = create_refresh_token(
        identity=identity,
        additional_claims=additional_claims,
    )

    return jsonify({
        "code": 200,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "expires_in": Config.JWT_ACCESS_TOKEN_EXPIRES,
        "user": {
            "user_id": user["user_id"],
            "username": user["username"],
            "full_name": user["full_name"],
            "email": user.get("email"),
            "role": user["role"],
        },
    }), 200


@app.route("/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    POST /auth/refresh
    Header: Authorization: Bearer <refresh_token>

    Response 200: { "code": 200, "access_token": "<JWT>", "expires_in": 3600 }
    """
    identity = get_jwt_identity()
    claims = get_jwt()

    additional_claims = {
        "username": claims.get("username"),
        "full_name": claims.get("full_name"),
        "email": claims.get("email"),
        "role": claims.get("role"),
    }

    new_access_token = create_access_token(
        identity=identity,
        additional_claims=additional_claims,
    )

    return jsonify({
        "code": 200,
        "access_token": new_access_token,
        "token_type": "Bearer",
        "expires_in": Config.JWT_ACCESS_TOKEN_EXPIRES,
    }), 200

@app.route("/auth/logout", methods=["POST"])
@jwt_required(refresh=True)
def logout():
    """
    POST /auth/logout
    Header: Authorization: Bearer <refresh_token>

    Thu hồi refresh_token (thêm vào blacklist).
    Response 200: { "code": 200, "message": "Đăng xuất thành công" }
    """
    jti: str = get_jwt()["jti"]
    _blacklist_token(jti)
    return jsonify({"code": 200, "message": "Đăng xuất thành công"}), 200
# =======================================================================
# ENDPOINT XEM THÔNG TIN NGƯỜI DÙNG HIỆN TẠI (ví dụ bảo vệ bằng JWT)
# =======================================================================
@app.route("/auth/me", methods=["GET"])
@jwt_required()
def me():
    """
    GET /auth/me
    Header: Authorization: Bearer <access_token>

    Trả về thông tin user đang đăng nhập (lấy từ JWT claims).
    """
    claims = get_jwt()
    return jsonify({
        "code": 200,
        "user": {
            "user_id": get_jwt_identity(),
            "username": claims.get("username"),
            "full_name": claims.get("full_name"),
            "email": claims.get("email"),
            "role": claims.get("role"),
        },
    }), 200
# =======================================================================
# ENDPOINT MẪU BẢO VỆ THEO ROLE / PERMISSION
# =======================================================================

@app.route("/admin/users", methods=["GET"])
@jwt_required()
@require_roles("ADMIN")
def admin_list_users():
    """Chỉ ADMIN được xem danh sách users."""
    mock_list = [
        {"user_id": u["user_id"], "username": u["username"], "role": u["role"]}
        for u in MOCK_USERS.values()
    ]
    return jsonify({"code": 200, "users": mock_list}), 200


@app.route("/subjects", methods=["GET"])
@jwt_required()
@require_permission("subject:read")
def list_subjects():
    """ADMIN, LECTURER, STUDENT đều có thể xem môn học."""
    return jsonify({
        "code": 200,
        "message": "Danh sách môn học (demo)",
        "subjects": [
            {"subject_code": "IT3040", "name": "Công nghệ phần mềm", "credits": 3},
            {"subject_code": "IT3010", "name": "Lập trình hướng đối tượng", "credits": 4},
        ],
    }), 200


@app.route("/subjects", methods=["POST"])
@jwt_required()
@require_permission("subject:create")
def create_subject():
    """Chỉ ADMIN mới có thể tạo môn học mới."""
    data = request.get_json(silent=True) or {}
    return jsonify({
        "code": 201,
        "message": f"Đã tạo môn học: {data.get('name', '(demo)')}",
    }), 201


@app.route("/registrations", methods=["POST"])
@jwt_required()
@require_permission("registration:create")
def register_section():
    """STUDENT (và ADMIN) có thể đăng ký học phần."""
    data = request.get_json(silent=True) or {}
    claims = get_jwt()
    return jsonify({
        "code": 201,
        "message": f"Sinh viên {claims.get('username')} đã đăng ký section_id={data.get('section_id')}",
    }), 201
# =======================================================================
# UTILITY: kiểm tra quyền hiện tại của token
# =======================================================================

@app.route("/auth/permissions", methods=["GET"])
@jwt_required()
def my_permissions():
    """Trả về toàn bộ quyền của người dùng đang đăng nhập."""
    claims = get_jwt()
    role: str = claims.get("role", "")
    perms = sorted(PERMISSIONS.get(role, set()))
    return jsonify({
        "code": 200,
        "role": role,
        "permissions": perms,
    }), 200

# =======================================================================
# ERROR HANDLERS
# =======================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({"code": 404, "message": "Endpoint không tồn tại"}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"code": 405, "message": "Phương thức HTTP không được phép"}), 405


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"code": 500, "message": "Lỗi server nội bộ"}), 500


# =======================================================================
# MAIN
# =======================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  QLDT Auth Module – SSO/JWT + RBAC")
    print("=" * 60)
    print(f"  Mock DB  : {Config.USE_MOCK_DB}")
    print(f"  JWT TTL  : access={Config.JWT_ACCESS_TOKEN_EXPIRES}s, "
          f"refresh={Config.JWT_REFRESH_TOKEN_EXPIRES}s")
    print(f"  URL      : http://localhost:{Config.PORT}")
    print("=" * 60)
    app.run(debug=Config.DEBUG, port=Config.PORT)
