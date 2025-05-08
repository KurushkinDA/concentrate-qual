from sqlalchemy.ext.asyncio import AsyncSession

from app.concentrate.dao import ConcentrateDAO
from app.concentrate.schemas import SConcentrateCreate, SConcentrateRead
from app.schemas import ResponseWithData


async def create_concentrate_service(
    session: AsyncSession, data: SConcentrateCreate, user_id: int
) -> ResponseWithData[SConcentrateRead]:
    """
    Создаёт запись с показателями концентрата в базе данных.

    Args:
        session: Асинхронная сессия SQLAlchemy.
        data: Данные для создания показателей.
        user_id: ID пользователя, добавившего показатели.

    Returns:
        ResponseWithData[SConcentrateRead]: Ответ с сообщением об
          успехе и созданными данными.
    """
    new_concentrate = await ConcentrateDAO.add(
        session,
        name=data.name,
        iron=data.iron,
        silicon=data.silicon,
        aluminum=data.aluminum,
        calcium=data.calcium,
        sulfur=data.sulfur,
        report_month=data.report_month,
        user_id=user_id,
    )
    return ResponseWithData(
        message="Показатели успешно добавлены",
        data=SConcentrateRead.model_validate(new_concentrate),
    )
