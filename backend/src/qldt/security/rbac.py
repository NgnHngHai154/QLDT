import inspect
from functools import wraps

from qldt.common.errors import error_response


def require_roles(*roles: str):
    """Protect a Sanic handler using the authenticated user's role."""
    def decorate(handler):
        if inspect.iscoroutinefunction(handler):
            @wraps(handler)
            async def async_wrapper(request, *args, **kwargs):
                user = getattr(request.ctx, "auth_user", None)
                if user is None:
                    return error_response(request, 401, "UNAUTHORIZED", "Đăng nhập để tiếp tục.")
                if user["role"] not in roles:
                    return error_response(request, 403, "FORBIDDEN", "Bạn không có quyền thực hiện thao tác này.")
                return await handler(request, *args, **kwargs)
            return async_wrapper

        @wraps(handler)
        def sync_wrapper(request, *args, **kwargs):
            user = getattr(request.ctx, "auth_user", None)
            if user is None:
                return error_response(request, 401, "UNAUTHORIZED", "Đăng nhập để tiếp tục.")
            if user["role"] not in roles:
                return error_response(request, 403, "FORBIDDEN", "Bạn không có quyền thực hiện thao tác này.")
            return handler(request, *args, **kwargs)
        return sync_wrapper
    return decorate