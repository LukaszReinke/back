from typing import Any
from uuid import UUID

from sqlalchemy.future import select
from models import WorkshopBase
from models.base import AsyncSession, transactional  # type: ignore
from sqlalchemy import Select, func
import controllers as ctrl


async def filters(query: Select[tuple[WorkshopBase]], params: ctrl.WorkshopQuery):

    if params.workshop_topic is not None:
        query = query.where(
            WorkshopBase.workshop_topic.ilike(f"%{params.workshop_topic}%")
        )

    if params.localization is not None:
        query = query.where(WorkshopBase.localization == params.localization)

    if params.start_date or params.end_date:
        conditions: list[Any] = []

        if params.start_date:
            conditions.append(WorkshopBase.start_date >= params.start_date)
        if params.end_date:
            conditions.append(WorkshopBase.end_date <= params.end_date)
        query = query.filter(*conditions)

    if params.categories is not None:
        query = query.where(WorkshopBase.categories == params.categories)

    # TO DO: strip price from str
    if params.price is not None:
        query = query.where(WorkshopBase.price == params.price)

    return query


class WorkshopRepository:

    @staticmethod
    @transactional
    async def get_workshop_by_id(workshop_id: UUID, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        workshop: WorkshopBase | None = await session.get(
            WorkshopBase,
            workshop_id,
        )
        return workshop

    @staticmethod
    @transactional
    async def add_workshop(workshop: WorkshopBase, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        session.add(workshop)

    @staticmethod
    @transactional
    async def update_workshop(workshop: WorkshopBase, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        await session.merge(workshop)

    @staticmethod
    @transactional
    async def get_all_workshops(**kwargs: Any):
        session: AsyncSession = kwargs["session"]
        result = await session.execute(select(WorkshopBase))
        return result.scalars().all()

    @staticmethod
    @transactional
    async def get_workshops(
        offset: int,
        per_page: int,
        params: ctrl.WorkshopQuery,
        is_approved: bool | None = None,
        **kwargs: Any,
    ):
        session: AsyncSession = kwargs["session"]
        query = select(WorkshopBase)

        if is_approved is not None:
            query = query.filter_by(is_approved=is_approved)

        query = await filters(query, params)

        query = query.offset(offset).limit(per_page)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    @transactional
    async def delete_workshop(workshop: WorkshopBase, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        await session.delete(workshop)

    @staticmethod
    @transactional
    async def get_workshop_by_column(
        column_name: str,
        value: Any,
        **kwargs: Any,
    ):
        session: AsyncSession = kwargs["session"]
        column = getattr(WorkshopBase, column_name, None)
        if column is None:
            raise ValueError(
                f"Column '{column_name}' does not exist in WorkshopBase.",
            )

        query = select(WorkshopBase).where(column == value)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    @transactional
    async def total_workshops(
        params: ctrl.WorkshopQuery,
        is_approved: bool | None = None,
        **kwargs: Any,
    ) -> Any:

        session: AsyncSession = kwargs["session"]
        query = select(WorkshopBase)

        if is_approved is not None:
            query = query.filter_by(is_approved=is_approved)

        query = await filters(query, params)

        result = await session.execute(
            select(func.count()).select_from(query.subquery())
        )
        return result.scalar_one()
