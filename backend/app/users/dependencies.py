from fastapi import Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.users.auth import create_access_token, decode_token, get_user_from_token
from app.users.dao import UserDAO
from app.users.exceptions import TokenExpiredException
from app.users.models import User


async def get_current_user(
    response: Response,
    request: Request,
    session: AsyncSession = Depends(get_db),
) -> User:
    """
    Получение текущего авторизованного пользователя по access_token

    Если access_token отсутствует или недействителен, но есть refresh_token,
    создаётся новый access_token и пользователь авторизуется повторно

    Args:
        response: HTTP-ответ для установки новых cookies
        session: Сессия SQLAlchemy для работы с БД
        access_token: JWT-токен авторизации (из cookies)
        refresh_token: JWT-токен обновления (из cookies)

    Returns:
        User: Объект пользователя, если токены валидны

    Raises:
        TokenExpiredException: Если пользователь не авторизован
    """

    access_token = request.cookies.get(f"{settings.PROJECT_NAME}_access_token")
    refresh_token = request.cookies.get(f"{settings.PROJECT_NAME}_refresh_token")

    user = None

    if access_token:
        try:
            user = await get_user_from_token(access_token, session)
        except Exception:
            user = None

    if not user and refresh_token:
        try:
            payload = decode_token(refresh_token)
            user_id = payload.get("sub")
            if user_id:
                user = await UserDAO.find_by_id(session, int(user_id))
                if user:
                    new_access_token = create_access_token({"sub": str(user.id)})
                    response.set_cookie(
                        f"{settings.PROJECT_NAME}_access_token",
                        new_access_token,
                        httponly=True,
                    )
        except Exception:
            user = None

    if not user:
        raise TokenExpiredException

    return user
