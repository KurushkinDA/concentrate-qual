from sqlalchemy import NullPool, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import settings

# Формирование URL
DATABASE_URL = settings.DATABASE_URL

# Настройки для тестов
if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_PARAMS = {}

# Async engine (FastAPI)
engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Базовый класс
class Base(DeclarativeBase):
    pass

# Зависимость FastAPI
async def get_db() -> AsyncSession:
    db = async_session_maker()
    try:
        yield db
    finally:
        await db.close()