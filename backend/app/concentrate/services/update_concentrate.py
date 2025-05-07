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
    concentrate = await ConcentrateDAO.find_by_id(session, concentrate_id)

    if not concentrate:
        raise ConcentrateNotFound

    updated = await ConcentrateDAO.update(session, concentrate_id, **data.model_dump())
    return ResponseWithData(
        message="Показатели успешно обновлены",
        data=SConcentrateRead.model_validate(updated)
    )