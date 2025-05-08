import os
os.environ["MODE"] = "TEST"

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient, ASGITransport

from app.main import app as fastapi_app
from app.core.database import async_session_maker, engine, Base
from app.core.config import settings
from scripts.init_users import main as init_users


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    # Пересоздание таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Запуск скрипта инициализации пользователей
    await init_users()


@pytest_asyncio.fixture()
async def async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture()
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app),
        base_url="http://test"
    ) as client:
        yield client