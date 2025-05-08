from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.schemas import SuccessResponse
from app.users.auth import authenticate_user, create_access_token, create_refresh_token
from app.users.exceptions import IncorrectUsernameOrPasswordException
from app.users.schemas import SUserAuth


async def login_user_service(
    user_data: SUserAuth, response: Response, session: AsyncSession
) -> SuccessResponse:
    """
    Аутентификация пользователя и установка токенов в куки.

    Args:
        user_data (SUserAuth): Данные пользователя (логин и пароль).
        response (Response): Объект ответа FastAPI для установки cookie.
        session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        SuccessResponse: Сообщение об успешной авторизации.

    Raises:
        IncorrectUsernameOrPasswordException: Если логин или пароль некорректны.
    """

    # Проверка аутентификации пользователя
    user = await authenticate_user(user_data.username, user_data.password, session)
    if not user:
        raise IncorrectUsernameOrPasswordException

    # Создание токенов
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    # Установка кук с токенами
    response.set_cookie(
        f"{settings.PROJECT_NAME}_access_token", access_token, httponly=True
    )
    response.set_cookie(
        f"{settings.PROJECT_NAME}_refresh_token", refresh_token, httponly=True
    )

    return SuccessResponse(message="Вы авторизовались")
