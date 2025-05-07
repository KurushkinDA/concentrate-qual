from app.concentrate.exceptions import ConcentrateNotFound
from sqlalchemy.ext.asyncio import AsyncSession
from app.concentrate.dao import ConcentrateDAO
from app.schemas import SuccessResponse

async def delete_concentrate_service(
    session: AsyncSession,
    concentrate_id: int,
) -> SuccessResponse:
    
    concentrate = await ConcentrateDAO.find_by_id(session, concentrate_id)
    if not concentrate:
        raise ConcentrateNotFound

    await ConcentrateDAO.delete(session, id=concentrate_id)
    return SuccessResponse(message="Показатели успешно удалены")