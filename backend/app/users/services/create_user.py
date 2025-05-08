from app.schemas import SuccessResponse
from app.users.dao import UserDAO
from app.users.exceptions import UserAlreadyExist, UserErrorCreate
from app.users.schemas import SUserCreate
from app.users.auth import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.models import User


async def create_user_service(data: SUserCreate, session: AsyncSession) -> User:
    """
    Создаёт нового пользователя в базе данных

    Проверяет, существует ли уже пользователь с таким логином.
    В случае отсутствия — хеширует пароль и добавляет пользователя в базу.

    Args:
        data: Данные для создания пользователя (username и password).
        session: Асинхронная сессия SQLAlchemy.

    Raises:
        UserAlreadyExist: Если пользователь с таким логином уже существует.
        UserErrorCreate: Если не удалось создать пользователя.

    Returns:
        SuccessResponse: Подтверждение успешного создания пользователя.
    """

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