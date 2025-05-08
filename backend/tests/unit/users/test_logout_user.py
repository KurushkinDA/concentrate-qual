import pytest
from fastapi import Response
from app.users.services.logout_user import logout_user_service
from app.core.config import settings

@pytest.mark.asyncio
async def test_logout_success():
    response = Response()

    cookie_key = f"{settings.PROJECT_NAME}_access_token"
    response.set_cookie(key=cookie_key, value="testtoken")

    await logout_user_service(response)

    # Получаем все Set-Cookie заголовки
    cookie_header = response.headers.getlist("set-cookie")
    # Проверяем, что есть удаление access_token с Max-Age=0
    assert any(
        cookie_key in header and ("max-age=0" in header.lower() or "expires=" in header.lower())
        for header in cookie_header
    )