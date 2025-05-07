from fastapi import Response
from app.core.config import settings
from app.schemas import SuccessResponse


async def logout_user_service(response: Response): 
    """
    Удаляет access и refresh токены из cookies, завершает сессию пользователя

    Args:
        response (Response): Объект ответа FastAPI, в который устанавливаются удаления cookies

    Returns:
        SuccessResponse: Успешный ответ с сообщением о выходе из аккаунта
    """
    response.delete_cookie(f"{settings.PROJECT_NAME}_access_token")
    response.delete_cookie(f"{settings.PROJECT_NAME}_refresh_token")
    
    return SuccessResponse(message="Вы вышли из аккаунта")