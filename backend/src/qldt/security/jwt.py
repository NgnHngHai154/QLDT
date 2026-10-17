from datetime import datetime, timedelta, timezone

import jwt


class TokenExpired(Exception):
    pass


class InvalidToken(Exception):
    pass


def create_access_token(user_id: int, role: str, secret: str, ttl_seconds: int = 3600) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "userId": user_id,
        "role": role,
        "iat": now,
        "exp": now + timedelta(seconds=ttl_seconds),
        "iss": "qldt",
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_access_token(token: str, secret: str) -> dict:
    try:
        return jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
            issuer="qldt",
            options={"require": ["sub", "userId", "role", "iat", "exp", "iss"]},
        )
    except jwt.ExpiredSignatureError as exc:
        raise TokenExpired from exc
    except jwt.InvalidTokenError as exc:
        raise InvalidToken from exc