from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from app.users.dao import UserDAO
from app.core.config import settings
from app.users.exceptions import IncorrectTokenFormatException, IncorrectUsernameOrPasswordException, TokenExpiredException
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Получение хешированного пароля

    Args: 
        password: пароль

    Returns: 
        str: хешированный пароль
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверка соответствия введённого пароля его хешу

    Args:
        plain_password: Обычный (введённый) пароль
        hashed_password: Хешированный пароль из базы данных

    Returns:
        bool: True, если пароль верный, иначе False
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Создание JWT access токена

    Args:
        data (dict): Данные пользователя, которые будут закодированы в токене

    Returns:
        str: access токен
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.AUTH_SECRET_KEY, algorithm=settings.AUTH_ALGORITHM
    )
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """
    Создание JWT refresh токена

    Args:
        data (dict): Данные пользователя, которые будут закодированы в токене

    Returns:
        str: refresh токен
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.AUTH_SECRET_KEY, algorithm=settings.AUTH_ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> dict:
    """
    Декодирует JWT токен и возвращает полезную нагрузку (payload)

    Args:
        token: токен

    Returns:
        dict: Распакованные данные

    Raises:
        TokenExpiredException: Если срок действия токена истёк
        IncorrectTokenFormatException: Если токен недействителен или имеет неверный формат
    """
    try:
        payload = jwt.decode(
            token, settings.AUTH_SECRET_KEY, algorithms=[settings.AUTH_ALGORITHM]
        )
        return payload
    
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException
    except jwt.PyJWTError:
        raise IncorrectTokenFormatException
    

async def get_user_from_token(token: str):
    """
    Извлекает пользователя из переданного JWT токена

    Args:
        token: токен

    Returns:
        User: Объект пользователя, соответствующий ID в токене

    Raises:
        IncorrectUsernameOrPasswordException: Если токен некорректен или пользователь не найден
    """
    payload = decode_token(token)

    user_id: str = payload.get("sub")
    if not user_id:
        raise IncorrectUsernameOrPasswordException
    
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise IncorrectUsernameOrPasswordException

    return user

async def authenticate_user(username: str, password: str, session: AsyncSession):
    """
    Проверяет логин и пароль, и возвращает пользователя, если они верны

    Args:
        username: Логин
        password: Обычный (нехэшированный) пароль
        session: Сессия 

    Returns:
        User | None: Объект пользователя, если аутентификация прошла успешно, иначе None
    """

    user = await UserDAO.find_one_or_none(session, username=username)
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user

      