from typing import Any
from sqlalchemy.future import select
from models import EventBase
from models.base import AsyncSession, transactional  # type: ignore


class EventRepository:

    @staticmethod
    @transactional
    async def get_event_by_id(event_id: int, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        event: EventBase | None = await session.get(
            EventBase,
            event_id,
        )
        return event

    @staticmethod
    @transactional
    async def add_event(event: EventBase, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        session.add(event)

    @staticmethod
    @transactional
    async def update_event(event: EventBase, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        await session.merge(event)

    @staticmethod
    @transactional
    async def get_all_events(**kwargs: Any):
        session: AsyncSession = kwargs["session"]
        result = await session.execute(select(EventBase))
        return result.scalars().all()

    @staticmethod
    @transactional
    async def get_events(
        name: str | None = None,
        is_approved: bool | None = None,
        category: str | None = None,
        **kwargs: Any,
    ):
        session: AsyncSession = kwargs["session"]
        query = select(EventBase)

        if category is not None:
            query = query.where(EventBase.category == category)

        if name is not None:
            query = query.where(EventBase.name.ilike(f"%{name}%"))

        if is_approved is not None:
            query = query.filter_by(is_approved=is_approved)

        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    @transactional
    async def delete_event(event: EventBase, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        await session.delete(event)

    @staticmethod
    @transactional
    async def get_event_by_column(
        column_name: str,
        value: Any,
        **kwargs: Any,
    ):
        session: AsyncSession = kwargs["session"]
        column = getattr(EventBase, column_name, None)
        if column is None:
            raise ValueError(
                f"Column '{column_name}' does not exist in EventBase.",
            )

        query = select(EventBase).where(column == value)
        result = await session.execute(query)
        return result.scalars().first()
