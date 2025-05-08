from app.concentrate.exceptions import ConcentrateNotFound
from sqlalchemy.ext.asyncio import AsyncSession
from app.concentrate.dao import ConcentrateDAO
from app.concentrate.schemas import SConcentrateUpdate, SConcentrateRead
from app.schemas import ResponseWithData

async def update_concentrate_service(
    concentrate_id: int,
    data: SConcentrateUpdate,
    session: AsyncSession,
) -> ResponseWithData[SConcentrateRead]:
    """
    Обновляет запись о показателях концентрата по заданному идентификатору.

    Args:
        concentrate_id: Идентификатор записи концентрата.
        data: Объект с обновлёнными данными.
        session: Асинхронная сессия SQLAlchemy.

    Returns:
        ResponseWithData[SConcentrateRead]: Объект с сообщением и обновлённой записью.

    Raises:
        ConcentrateNotFound: Если запись с указанным ID не найдена.
    """
    concentrate = await ConcentrateDAO.find_by_id(session, concentrate_id)

    if not concentrate:
        raise ConcentrateNotFound

    updated = await ConcentrateDAO.update(session, concentrate_id, **data.model_dump())
    return ResponseWithData(
        message="Показатели успешно обновлены",
        data=SConcentrateRead.model_validate(updated)
    )