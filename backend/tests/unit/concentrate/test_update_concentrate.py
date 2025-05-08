import pytest
from app.users.schemas import SUserCreate
from app.users.services.create_user import create_user_service
from app.users.dao import UserDAO
from app.concentrate.schemas import SConcentrateCreate, SConcentrateUpdate
from app.concentrate.services.create_concentrate import create_concentrate_service
from app.concentrate.services.update_concentrate import update_concentrate_service
from app.concentrate.services.get_concentrate_by_id import get_concentrate_by_id_service


@pytest.mark.asyncio
async def test_update_concentrate(async_session):
    # Создание пользователя
    user_data = SUserCreate(username="updater", password="securepass")
    await create_user_service(user_data, async_session)
    user = await UserDAO.find_one_or_none(async_session, username=user_data.username)

    # Создание записи
    initial_data = SConcentrateCreate(
        name="Initial Conc",
        iron=10.0,
        silicon=5.0,
        aluminum=3.0,
        calcium=2.0,
        sulfur=1.0,
        report_month="2025-05"
    )
    create_result = await create_concentrate_service(async_session, initial_data, user.id)

    # Обновление записи
    update_data = SConcentrateUpdate(
        name="Updated Conc",
        iron=15.0,
        silicon=6.0,
        aluminum=4.0,
        calcium=3.0,
        sulfur=2.0,
        report_month="2025-06"
    )
    update_result = await update_concentrate_service(
        concentrate_id=create_result.data.id,
        data=update_data,
        session=async_session
    )

    # Проверка данных после обновления
    assert update_result.data.name == "Updated Conc"
    assert update_result.data.iron == 15.0
    assert update_result.data.silicon == 6.0
    assert update_result.data.aluminum == 4.0
    assert update_result.data.calcium == 3.0
    assert update_result.data.sulfur == 2.0
    assert update_result.data.report_month == "2025-06"
    assert update_result.data.user.username == "updater"

    # Получение и проверка записи из БД
    from_db = await get_concentrate_by_id_service(update_result.data.id, async_session)
    assert from_db.data.name == "Updated Conc"
    assert from_db.data.iron == 15.0
    assert from_db.data.silicon == 6.0
    assert from_db.data.aluminum == 4.0
    assert from_db.data.calcium == 3.0
    assert from_db.data.sulfur == 2.0
    assert from_db.data.report_month == "2025-06"
    assert from_db.data.user.username == "updater"