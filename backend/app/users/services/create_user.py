from app.schemas import SuccessResponse
from app.users.dao import UserDAO
from app.users.exceptions import UserAlreadyExist, UserErrorCreate
from app.users.schemas import SUserCreate
from app.users.auth import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.models import User


async def create_user_service(data: SUserCreate, session: AsyncSession) -> User:
    
    # Проверка пользователя с таким логином
    has_username = await UserDAO.find_one_or_none(session, username=data.username)
    if has_username: 
        raise UserAlreadyExist
    
    # Хеширование пароля
    hashed_password = get_password_hash(data.password)
    
    # Создание пользователя
    user = await UserDAO.add(
        session,
        username=data.username,
        hashed_password=hashed_password
    )

    # Проверка, что пользователь создался
    if not user: 
        raise UserErrorCreate

    return SuccessResponse(message="Пользователь успешно создан")