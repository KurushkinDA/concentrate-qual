import pytest

from app.concentrate.schemas import SConcentrateCreate
from app.concentrate.services.create_concentrate import create_concentrate_service
from app.concentrate.services.get_concentrate_statistics import get_concentrate_statistics_service
from app.users.schemas import SUserCreate
from app.users.services.create_user import create_user_service
from app.users.dao import UserDAO


@pytest.mark.asyncio
async def test_get_concentrate_statistics(async_session):
    # Создание пользователя
    user_data = SUserCreate(username="statuser", password="statpass")
    await create_user_service(user_data, async_session)
    user = await UserDAO.find_one_or_none(async_session, username=user_data.username)

    # Добавление двух записей концентрата
    await create_concentrate_service(async_session, SConcentrateCreate(
        name="Stat A", iron=10.0, silicon=20.0, aluminum=30.0, calcium=40.0, sulfur=50.0,
        report_month="2025-05"
    ), user.id)
    await create_concentrate_service(async_session, SConcentrateCreate(
        name="Stat B", iron=11.0, silicon=21.0, aluminum=31.0, calcium=41.0, sulfur=51.0,
        report_month="2025-05"
    ), user.id)

    # Получение статистики
    stats = await get_concentrate_statistics_service(async_session, report_month="2025-05")

    # Проверка основных значений
    assert stats.data.average_iron == 10.5
    assert stats.data.min_sulfur == 50.0
    assert stats.data.max_sulfur == 51.0
    assert stats.data.average_silicon == 20.5
    assert stats.data.average_aluminum == 30.5