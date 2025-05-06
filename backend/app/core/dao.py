from typing import TypeVar, Generic, Type, Optional, Sequence, List
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")

class BaseDAO(Generic[T]):
    model: Type[T]

    @classmethod
    async def find_by_id(cls, session: AsyncSession, model_id: int) -> Optional[T]:
        query = select(cls.model).filter_by(id=model_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filters) -> Optional[T]:
        query = select(cls.model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, session: AsyncSession, **filters) -> Sequence[T]:
        query = select(cls.model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_by_ids(cls, session: AsyncSession, ids: List[int]) -> Sequence[T]:
        query = select(cls.model).where(cls.model.id.in_(ids))  # type: ignore[attr-defined]
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def add(cls, session: AsyncSession, **data) -> T:
        stmt = insert(cls.model).values(**data).returning(cls.model)
        result = await session.execute(stmt)
        await session.commit()
        return result.scalar_one()

    @classmethod
    async def update(cls, session: AsyncSession, model_id: int, **data) -> Optional[T]:
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
        obj = await cls.find_one_or_none(session, **filters)
        if not obj:
            return None
        await session.delete(obj)
        await session.commit()
        return obj