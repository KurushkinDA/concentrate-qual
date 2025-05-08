import re

from sqlalchemy.ext.asyncio import AsyncSession

from app.concentrate.dao import ConcentrateDAO
from app.concentrate.exceptions import NoDataFound, WrongFormatDate
from app.concentrate.schemas import SConcentrateStats
from app.schemas import ResponseWithData


async def get_concentrate_statistics_service(
    session: AsyncSession,
    report_month: str,
) -> ResponseWithData[SConcentrateStats]:
    """
    Формирует статистику по показателям концентрата за указанный месяц.

    Args:
        session: Асинхронная сессия SQLAlchemy.
        report_month: Месяц в формате "YYYY-MM", по которому формируется отчёт.

    Returns:
        ResponseWithData[SConcentrateStats]: Объект с сообщением и
          статистическими данными.

    Raises:
        WrongFormatDate: Если передан неверный формат месяца.
        NoDataFound: Если по выбранному месяцу нет данных.
    """
    if not re.fullmatch(r"\d{4}-\d{2}", report_month):
        raise WrongFormatDate

    data = await ConcentrateDAO.get_monthly_statistics(session, report_month)

    if all(value is None for value in data.values()):
        raise NoDataFound

    stats = SConcentrateStats.model_validate(data)
    return ResponseWithData(message="Отчёт успешно сформирован", data=stats)
