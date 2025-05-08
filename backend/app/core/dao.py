"""
BaseDAO — универсальный базовый класс для работы с базой данных.

Реализует общие методы CRUD:
- Поиск по ID и фильтрам
- Добавление, обновление и удаление записей
- Поддерживает опции joinedload и фильтрацию по нескольким ID

Все методы работают асинхронно с использованием SQLAlchemy AsyncSession.
"""

from typing import Generic, List, Optional, Sequence, Type, TypeVar

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseDAO(Generic[T]):
    model: Type[T]

    @classmethod
    async def find_by_id(cls, session: AsyncSession, model_id: int) -> Optional[T]:
        """Найти одну запись по ID."""
        query = select(cls.model).filter_by(id=model_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filters) -> Optional[T]:
        """Найти одну запись по фильтрам. Вернёт None, если не найдено."""
        query = select(cls.model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_all(
        cls, session: AsyncSession, options: Optional[list] = None, **filters
    ) -> Sequence[T]:
        """
        Найти все записи по фильтрам. Поддерживает опции (например, joinedload).
        """
        query = select(cls.model)
        if options:
            query = query.options(*options)
        if filters:
            query = query.filter_by(**filters)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_by_ids(cls, session: AsyncSession, ids: List[int]) -> Sequence[T]:
        """Найти все записи, ID которых входят в указанный список."""
        query = select(cls.model).where(cls.model.id.in_(ids))  # type: ignore
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def add(cls, session: AsyncSession, **data) -> T:
        """
        Добавить новую запись в таблицу. Возвращает созданную модель.
        """
        stmt = insert(cls.model).values(**data).returning(cls.model)
        result = await session.execute(stmt)
        await session.commit()
        return result.scalar_one()

    @classmethod
    async def update(cls, session: AsyncSession, model_id: int, **data) -> Optional[T]:
        """
        Обновить запись по ID. Возвращает обновлённую запись или None, если не найдена.
        """
        obj = await cls.find_by_id(session, model_id)
        if not obj:
            return None
        for key, value in data.items():
            setattr(obj, key, value)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    async def delete(cls, session: AsyncSession, **filters) -> Optional[T]:
        """
        Удалить одну запись по фильтрам. Возвращает удалённую запись или None.
        """
        obj = await cls.find_one_or_none(session, **filters)
        if not obj:
            return None
        await session.delete(obj)
        await session.commit()
        return obj
