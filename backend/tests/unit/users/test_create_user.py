from app.users.models import User
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.schemas import SUserCreate
from app.users.services.create_user import create_user_service
from app.users.dao import UserDAO
from app.users.exceptions import UserAlreadyExist


@pytest.mark.asyncio
async def test_create_user_success(async_session: AsyncSession):
    user_data = SUserCreate(username="newuser", password="password123")
    await create_user_service(user_data, async_session)

    # Проверяем, что пользователь появился в БД
    user = await UserDAO.find_one_or_none(async_session, username="newuser")
    assert user is not None
    assert isinstance(user, User)
    assert user.username == "newuser"
    
    # Убедимся, что пароль захеширован
    assert user.hashed_password != "password123"
    assert user.hashed_password.startswith("$2b$")  # bcrypt hash

