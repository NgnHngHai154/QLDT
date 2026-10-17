from datetime import datetime, timedelta, timezone

from sanic.response import json

VIETNAM_TZ = timezone(timedelta(hours=7))


def error_response(request, status: int, error: str, message: str, details=None):
    return json(
        {
            "status": status,
            "error": error,
            "message": message,
            "details": details or [],
            "path": request.path,
            "timestamp": datetime.now(VIETNAM_TZ).isoformat(timespec="seconds"),
        },
        status=status,
    )