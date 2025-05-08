import pytest
from fastapi import HTTPException

from app.concentrate.schemas import SConcentrateCreate
from app.concentrate.services.create_concentrate import create_concentrate_service
from app.concentrate.services.delete_concentrate import delete_concentrate_service
from app.concentrate.services.get_concentrate_by_id import get_concentrate_by_id_service
from app.users.schemas import SUserCreate
from app.users.services.create_user import create_user_service
from app.users.dao import UserDAO


@pytest.mark.asyncio
async def test_delete_concentrate(async_session):
    # Создание пользователя
    user_data = SUserCreate(username="deleter", password="deletepass")
    await create_user_service(user_data, async_session)
    user = await UserDAO.find_one_or_none(async_session, username=user_data.username)

    # Создание записи
    data = SConcentrateCreate(
        name="To be deleted",
        iron=1.0,
        silicon=1.0,
        aluminum=1.0,
        calcium=1.0,
        sulfur=1.0,
        report_month="2025-05"
    )
    concentrate = await create_concentrate_service(async_session, data, user.id)

    # Удаление записи
    await delete_concentrate_service(async_session, concentrate.data.id)

    # Проверка: запись должна отсутствовать
    try:
        await get_concentrate_by_id_service(concentrate.data.id, async_session)
        assert False, "Ожидалась ошибка, но запись была найдена"
    except HTTPException as exc:
        assert exc.status_code == 404