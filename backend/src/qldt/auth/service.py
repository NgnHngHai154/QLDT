import bcrypt

from qldt.security.jwt import create_access_token


class AuthenticationFailure(Exception):
    def __init__(self, status: int, error: str, message: str, details=None):
        self.status = status
        self.error = error
        self.message = message
        self.details = details or []


def public_user(user: dict) -> dict:
    return {
        "userId": user["user_id"],
        "username": user["username"],
        "fullName": user["full_name"],
        "email": user.get("email"),
        "role": user["role"],
    }


class AuthenticationService:
    def __init__(self, user_repository, settings):
        self._user_repository = user_repository
        self._settings = settings

    async def login(self, username: str, password: str) -> dict:
        user = await self._user_repository.find_by_username(username)
        if user is None:
            raise AuthenticationFailure(401, "INVALID_CREDENTIALS", "Tên đăng nhập hoặc mật khẩu không đúng.")

        try:
            valid_password = bcrypt.checkpw(
                password.encode("utf-8"),
                user["password_hash"].encode("utf-8"),
            )
        except (ValueError, TypeError):
            valid_password = False

        if not valid_password:
            raise AuthenticationFailure(401, "INVALID_CREDENTIALS", "Tên đăng nhập hoặc mật khẩu không đúng.")
        if user["status"] == "LOCKED":
            raise AuthenticationFailure(403, "ACCOUNT_LOCKED", "Tài khoản đang bị khóa.")

        access_token = create_access_token(
            user_id=user["user_id"],
            role=user["role"],
            secret=self._settings.jwt_secret_key,
            ttl_seconds=self._settings.access_token_ttl_seconds,
        )
        return {
            "accessToken": access_token,
            "tokenType": "Bearer",
            "expiresIn": self._settings.access_token_ttl_seconds,
            "user": public_user(user),
        }

    async def get_active_user(self, user_id: int) -> dict | None:
        user = await self._user_repository.find_by_id(user_id)
        if user is None or user["status"] != "ACTIVE":
            return None
        return public_user(user)