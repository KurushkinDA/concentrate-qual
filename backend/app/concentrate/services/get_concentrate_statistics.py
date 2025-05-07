import re
from app.concentrate.dao import ConcentrateDAO
from app.concentrate.exceptions import NoDataFound, WrongFormatDate
from app.concentrate.models import Concentrate
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.concentrate.schemas import SConcentrateStats
from app.schemas import ResponseWithData


async def get_concentrate_statistics_service(
    session: AsyncSession,
    report_month: str,
) -> ResponseWithData[SConcentrateStats]:
    if not re.fullmatch(r"\d{4}-\d{2}", report_month):
        raise WrongFormatDate

    data = await ConcentrateDAO.get_monthly_statistics(session, report_month)

    if all(value is None for value in data.values()):
        raise NoDataFound

    stats = SConcentrateStats.model_validate(data)
    return ResponseWithData(
        message="Отчёт успешно сформирован",
        data=stats
    )