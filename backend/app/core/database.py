"""
Настройка подключения к базе данных (PostgreSQL) с использованием SQLAlchemy (async).

- Поддерживает режимы DEV и TEST.
- Используется NullPool для тестов, чтобы избежать подключения к пулам.
- Предоставляет async_session_maker для создания сессий.
- Base — базовый класс для моделей.
- get_db — зависимость FastAPI для получения сессии.
"""

from sqlalchemy import NullPool, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import settings

# Формирование URL подключения в зависимости от режима
DATABASE_URL = settings.DATABASE_URL

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_PARAMS = {}

# Создание async-движка и фабрики сессий
engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Базовый класс для всех моделей
class Base(DeclarativeBase):
    """Базовый класс для декларативных моделей SQLAlchemy."""
    pass

# Зависимость для FastAPI — предоставляет асинхронную сессию
async def get_db() -> AsyncSession:
    """
    Зависимость FastAPI для получения асинхронной сессии базы данных.
    Закрывает сессию после завершения запроса.
    """
    db = async_session_maker()
    try:
        yield db
    finally:
        await db.close()