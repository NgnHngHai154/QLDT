from sanic import Blueprint
from sanic.response import json

from qldt.auth.service import AuthenticationFailure
from qldt.common.errors import error_response
from qldt.security.jwt import InvalidToken, TokenExpired, decode_access_token

auth_blueprint = Blueprint("auth", url_prefix="/api/auth")


async def load_authenticated_user(request):
    request.ctx.auth_user = None
    if request.path == "/api/auth/login":
        return None

    authorization = request.headers.get("authorization", "")
    if not authorization:
        return None

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return error_response(request, 401, "UNAUTHORIZED", "Authorization header không hợp lệ.")

    try:
        claims = decode_access_token(token, request.app.ctx.settings.jwt_secret_key)
        user = await request.app.ctx.auth_service.get_active_user(int(claims["userId"]))
    except TokenExpired:
        return error_response(request, 401, "TOKEN_EXPIRED", "Phiên đăng nhập đã hết hạn.")
    except (InvalidToken, KeyError, TypeError, ValueError):
        return error_response(request, 401, "UNAUTHORIZED", "Token không hợp lệ.")
    except Exception:
        return error_response(request, 500, "INTERNAL_SERVER_ERROR", "Không thể xử lý yêu cầu lúc này.")

    if user is None:
        return error_response(request, 401, "UNAUTHORIZED", "Tài khoản không còn hoạt động.")
    request.ctx.auth_user = user
    return None


@auth_blueprint.post("/login")
async def login(request):
    data = request.json if isinstance(request.json, dict) else {}
    username = data.get("username")
    password = data.get("password")
    details = []
    if not isinstance(username, str) or not username.strip():
        details.append({"field": "username", "message": "Tên đăng nhập là bắt buộc."})
    if not isinstance(password, str) or not password:
        details.append({"field": "password", "message": "Mật khẩu là bắt buộc."})
    if details:
        return error_response(request, 400, "VALIDATION_ERROR", "Dữ liệu đăng nhập không hợp lệ.", details)

    try:
        credentials = await request.app.ctx.auth_service.login(username.strip(), password)
    except AuthenticationFailure as failure:
        return error_response(request, failure.status, failure.error, failure.message, failure.details)
    except Exception:
        return error_response(request, 500, "INTERNAL_SERVER_ERROR", "Không thể xử lý yêu cầu lúc này.")

    return json({"status": 200, **credentials}, status=200)


@auth_blueprint.get("/me")
async def current_user(request):
    user = getattr(request.ctx, "auth_user", None)
    if user is None:
        return error_response(request, 401, "UNAUTHORIZED", "Đăng nhập để tiếp tục.")
    return json({"user": user}, status=200)