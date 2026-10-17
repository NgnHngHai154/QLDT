import asyncio

import mysql.connector


class DatabaseUnavailable(Exception):
    """Raised when the configured database cannot serve an auth request."""


class MySQLUserRepository:
    def __init__(self, settings):
        self._settings = settings

    async def find_by_username(self, username: str):
        return await asyncio.to_thread(self._find, "username", username)

    async def find_by_id(self, user_id: int):
        return await asyncio.to_thread(self._find, "user_id", user_id)

    def _find(self, column: str, value):
        if column not in {"username", "user_id"}:
            raise ValueError("Unsupported user lookup column.")

        connection = None
        cursor = None
        try:
            connection = mysql.connector.connect(
                host=self._settings.db_host,
                port=self._settings.db_port,
                database=self._settings.db_name,
                user=self._settings.db_user,
                password=self._settings.db_password,
                charset="utf8mb4",
                collation="utf8mb4_unicode_ci",
                connection_timeout=5,
            )
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT user_id, username, password_hash, full_name, email, role, status "
                f"FROM USERS WHERE {column} = %s LIMIT 1",
                (value,),
            )
            return cursor.fetchone()
        except mysql.connector.Error as exc:
            raise DatabaseUnavailable from exc
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()