from fastapi import APIRouter, Response, status

from app.core.database import DbSession
from app.dto.auth.auth import AuthResponse, CurrentUserResponse, LoginRequest
from app.security.dependencies import CurrentUser
from app.service.auth.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AuthResponse, summary="Đăng nhập (UC001)")
def login(body: LoginRequest, db: DbSession):
    return AuthService(db).login(body)


@router.get("/me", response_model=CurrentUserResponse, summary="Thông tin người dùng hiện tại")
def me(user: CurrentUser):
    return {"user": AuthService.to_user_info(user)}


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Đăng xuất",
)
def logout(user: CurrentUser):
    # JWT không lưu trạng thái; client tự xóa token.
    return Response(status_code=status.HTTP_204_NO_CONTENT)
