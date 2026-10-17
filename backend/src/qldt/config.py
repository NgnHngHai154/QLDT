import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    jwt_secret_key: str
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "qldt"
    db_user: str = "root"
    db_password: str = ""
    access_token_ttl_seconds: int = 3600

    @classmethod
    def from_env(cls):
        secret = os.getenv("JWT_SECRET_KEY", "")
        if len(secret.encode("utf-8")) < 32:
            raise ValueError("JWT_SECRET_KEY must be configured with at least 32 bytes.")
        return cls(
            jwt_secret_key=secret,
            db_host=os.getenv("DB_HOST", "localhost"),
            db_port=int(os.getenv("DB_PORT", "3306")),
            db_name=os.getenv("DB_NAME", "qldt"),
            db_user=os.getenv("DB_USER", "root"),
            db_password=os.getenv("DB_PASSWORD", ""),
        )