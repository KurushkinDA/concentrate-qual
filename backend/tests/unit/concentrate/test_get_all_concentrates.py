import pytest

from app.concentrate.schemas import SConcentrateCreate
from app.concentrate.services.create_concentrate import create_concentrate_service
from app.concentrate.services.get_all_concentrates import get_all_concentrates_service
from app.users.schemas import SUserCreate
from app.users.services.create_user import create_user_service
from app.users.dao import UserDAO


@pytest.mark.asyncio
async def test_get_all_concentrates(async_session):
    # Создание пользователя
    user_data = SUserCreate(username="alluser", password="strong123")
    await create_user_service(user_data, async_session)
    user = await UserDAO.find_one_or_none(async_session, username=user_data.username)

    # Добавление нескольких записей концентрата
    for i in range(2):
        await create_concentrate_service(
            async_session,
            SConcentrateCreate(
                name=f"Conc {i}",
                iron=float(i),
                silicon=float(i),
                aluminum=float(i),
                calcium=float(i),
                sulfur=float(i),
                report_month="2025-04"
            ),
            user.id
        )

    # Получение всех записей по месяцу
    result = await get_all_concentrates_service(async_session, report_month="2025-04")

    # Проверка количества найденных записей
    assert len(result.items) == 2
    assert all(item.report_month == "2025-04" for item in result.items)
    assert result.items[0].user.username == "alluser"