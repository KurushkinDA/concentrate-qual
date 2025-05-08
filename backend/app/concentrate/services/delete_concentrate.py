from sqlalchemy.ext.asyncio import AsyncSession

from app.concentrate.dao import ConcentrateDAO
from app.concentrate.exceptions import ConcentrateNotFound
from app.schemas import SuccessResponse


async def delete_concentrate_service(
    session: AsyncSession,
    concentrate_id: int,
) -> SuccessResponse:
    """
    Удаляет запись с показателями концентрата по её ID.

    Args:
        session: Асинхронная сессия SQLAlchemy.
        concentrate_id: Идентификатор записи для удаления.

    Returns:
        SuccessResponse: Ответ с сообщением об успешном удалении.

    Raises:
        ConcentrateNotFound: Если запись с таким ID не найдена.
    """
    concentrate = await ConcentrateDAO.find_by_id(session, concentrate_id)
    if not concentrate:
        raise ConcentrateNotFound

    await ConcentrateDAO.delete(session, id=concentrate_id)
    return SuccessResponse(message="Показатели успешно удалены")
