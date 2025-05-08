from app.concentrate.schemas import SConcentrateCreate
from app.concentrate.services.create_concentrate import create_concentrate_service
from app.concentrate.services.get_concentrate_by_id import get_concentrate_by_id_service
from app.users.dao import UserDAO
from app.users.schemas import SUserCreate
from app.users.services.create_user import create_user_service
import pytest





@pytest.mark.asyncio
async def test_create_and_get_concentrate(async_session):
    # Создание и получение пользователя
    user_data = SUserCreate(username="conc_user", password="strongpass")
    await create_user_service(user_data, async_session)
    user = await UserDAO.find_one_or_none(async_session, username=user_data.username)
    
    # Формирование записи
    data = SConcentrateCreate(
        name="Тест",
        iron=10.0,
        silicon=5.0,
        aluminum=3.0,
        calcium=2.0,
        sulfur=1.0,
        report_month="2025-05"
    )

    # Создание записи и получение ответа
    result = await create_concentrate_service(async_session, data, user.id)

    # Проверка ответа после создания
    assert result.data.name == "Тест"
    assert result.data.user.username == "conc_user"
    assert result.data.iron == 10.0
    assert result.data.silicon == 5.0
    assert result.data.aluminum == 3.0
    assert result.data.calcium == 2.0
    assert result.data.sulfur == 1.0
    assert result.data.report_month == "2025-05"

    # Запрос записи по id и проверка 
    found = await get_concentrate_by_id_service(result.data.id, async_session)
    assert found.data.name == "Тест"
    assert found.data.user.username == "conc_user"
    assert found.data.iron == 10.0
    assert found.data.silicon == 5.0
    assert found.data.aluminum == 3.0
    assert found.data.calcium == 2.0
    assert found.data.sulfur == 1.0
    assert found.data.report_month == "2025-05"