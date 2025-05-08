from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import SuccessResponse
from app.users.schemas import SUserAuth, SUserCreate
from app.users.services.create_user import create_user_service
from app.users.services.login_user import login_user_service
from app.users.services.logout_user import logout_user_service
from app.core.database import get_db

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post(
    "/login",
    summary="Авторизоваться",
    description="Выполнить вход по логину и паролю. Устанавливает куки с токеном.",
    response_model=SuccessResponse,
)
async def login_user(
    response: Response,
    user_data: SUserAuth,
    session: AsyncSession = Depends(get_db)
):
    return await login_user_service(user_data, response, session)


@router.post(
    "/logout",
    summary="Выйти из аккаунта",
    description="Удаляет токен авторизации из куки и завершает сессию.",
    response_model=SuccessResponse,
)
async def logout_user(response: Response):
    return await logout_user_service(response)