from app.concentrate.exceptions import ConcentrateNotFound
from sqlalchemy.ext.asyncio import AsyncSession
from app.concentrate.dao import ConcentrateDAO
from app.concentrate.schemas import SConcentrateRead
from app.schemas import ResponseWithData

async def get_concentrate_by_id_service(
    concentrate_id: int,
    session: AsyncSession
) -> ResponseWithData[SConcentrateRead]:
    """
    Получает одну запись концентрата по её ID.

    Args:
        concentrate_id: Идентификатор записи концентрата.
        session: Асинхронная сессия SQLAlchemy.

    Returns:
        ResponseWithData[SConcentrateRead]: Объект с сообщением и данными найденной записи.

    Raises:
        ConcentrateNotFound: Если запись с указанным ID не найдена.
    """
    concentrate = await ConcentrateDAO.find_by_id(session, concentrate_id)
    
    if not concentrate:
        raise ConcentrateNotFound
    
    return ResponseWithData(
        message="Запись найдена",
        data=SConcentrateRead.model_validate(concentrate)
    )