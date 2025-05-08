from sqlalchemy.ext.asyncio import AsyncSession
from app.concentrate.dao import ConcentrateDAO
from app.concentrate.models import Concentrate
from app.concentrate.schemas import SConcentrateRead
from sqlalchemy.orm import joinedload
from app.schemas import PaginatedResponse
from typing import List

async def get_all_concentrates_service(
    session: AsyncSession,
    report_month: str | None = None
) -> PaginatedResponse[SConcentrateRead]:
    """
    Получает список всех записей концентрата, с фильтрацией по месяцу (если указан).

    Args:
        session: Асинхронная сессия SQLAlchemy.
        report_month: Месяц в формате 'YYYY-MM' для фильтрации (опционально).

    Returns:
        PaginatedResponse[SConcentrateRead]: Список записей в формате пагинации.
    """
    filters = {}
    if report_month:
        filters["report_month"] = report_month

    concentrates = await ConcentrateDAO.find_all(
        session,
        options=[joinedload(Concentrate.user)],
        **filters
    )
    return PaginatedResponse(
        items=[SConcentrateRead.model_validate(c) for c in concentrates]
    )