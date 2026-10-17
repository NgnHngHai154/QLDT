from sanic import Sanic
from sanic.exceptions import MethodNotSupported, NotFound

from qldt.auth.repository import MySQLUserRepository
from qldt.auth.routes import auth_blueprint, load_authenticated_user
from qldt.auth.service import AuthenticationService
from qldt.config import Settings
from qldt.common.errors import error_response


def create_app(settings: Settings | None = None, user_repository=None, name: str = "qldt-backend") -> Sanic:
    settings = settings or Settings.from_env()
    app = Sanic(name, configure_logging=False)
    app.ctx.settings = settings
    app.ctx.user_repository = user_repository or MySQLUserRepository(settings)
    app.ctx.auth_service = AuthenticationService(app.ctx.user_repository, settings)
    app.middleware("request")(load_authenticated_user)
    app.blueprint(auth_blueprint)

    @app.exception(NotFound)
    async def handle_not_found(request, exception):
        return error_response(request, 404, "NOT_FOUND", "Endpoint không tồn tại.")

    @app.exception(MethodNotSupported)
    async def handle_method_not_allowed(request, exception):
        return error_response(request, 405, "METHOD_NOT_ALLOWED", "Phương thức HTTP không được hỗ trợ.")

    @app.exception(Exception)
    async def handle_unexpected_error(request, exception):
        return error_response(request, 500, "INTERNAL_SERVER_ERROR", "Không thể xử lý yêu cầu lúc này.")

    return app