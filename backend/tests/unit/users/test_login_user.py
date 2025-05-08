import pytest
from app.users.schemas import SUserAuth, SUserCreate
from app.users.services.login_user import login_user_service
from app.users.services.create_user import create_user_service
from app.users.exceptions import IncorrectUsernameOrPasswordException
from fastapi import Response
from app.core.config import settings


@pytest.mark.asyncio
async def test_login_success(async_session):
    await create_user_service(SUserCreate(username="loguser", password="pass123"), async_session)
    response = Response()
    await login_user_service(SUserAuth(username="loguser", password="pass123"), response, async_session)

    cookies = response.headers.get("set-cookie", "")
    assert f"{settings.PROJECT_NAME}_access_token=" in cookies


@pytest.mark.asyncio
async def test_login_wrong_credentials(async_session):
    await create_user_service(SUserCreate(username="wronguser", password="rightpass"), async_session)
    response = Response()

    with pytest.raises(type(IncorrectUsernameOrPasswordException)):
        await login_user_service(SUserAuth(username="wronguser", password="wrongpass"), response, async_session)