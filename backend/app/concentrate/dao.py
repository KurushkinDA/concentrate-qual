from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.concentrate.models import Concentrate
from app.core.dao import BaseDAO


class ConcentrateDAO(BaseDAO[Concentrate]):
    model = Concentrate

    @classmethod
    async def get_monthly_statistics(
        cls, session: AsyncSession, report_month: str
    ) -> dict:
        """
        Возвращает статистику (среднее, минимум, максимум) по каждому показателю
        концентрата за указанный месяц.

        Args:
            session: Асинхронная сессия SQLAlchemy.
            report_month: Месяц в формате "YYYY-MM".

        Returns:
            dict: Словарь со статистикой по каждому полю.
        """
        stmt = select(
            func.avg(cls.model.iron).label("average_iron"),
            func.min(cls.model.iron).label("min_iron"),
            func.max(cls.model.iron).label("max_iron"),
            func.avg(cls.model.silicon).label("average_silicon"),
            func.min(cls.model.silicon).label("min_silicon"),
            func.max(cls.model.silicon).label("max_silicon"),
            func.avg(cls.model.aluminum).label("average_aluminum"),
            func.min(cls.model.aluminum).label("min_aluminum"),
            func.max(cls.model.aluminum).label("max_aluminum"),
            func.avg(cls.model.calcium).label("average_calcium"),
            func.min(cls.model.calcium).label("min_calcium"),
            func.max(cls.model.calcium).label("max_calcium"),
            func.avg(cls.model.sulfur).label("average_sulfur"),
            func.min(cls.model.sulfur).label("min_sulfur"),
            func.max(cls.model.sulfur).label("max_sulfur"),
        ).where(cls.model.report_month == report_month)

        result = await session.execute(stmt)
        return result.one()._asdict()
