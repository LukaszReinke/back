from typing import Any
from sqlalchemy.future import select
from models import ContestBase
from models.base import AsyncSession, transactional  # type: ignore
from sqlalchemy import Select, func
from uuid import UUID
import controllers as ctrl


async def filters(query: Select[tuple[ContestBase]], params: ctrl.ContestQuery):

    if params.contest_name is not None:
        query = query.where(ContestBase.contest_name.ilike(f"%{params.contest_name}%"))

    if params.localization is not None:
        query = query.where(ContestBase.localization == params.localization)

    if params.start_date or params.end_date:
        conditions: list[Any] = []

        if params.start_date:
            conditions.append(ContestBase.start_date >= params.start_date)
        if params.end_date:
            conditions.append(ContestBase.end_date <= params.end_date)
        query = query.filter(*conditions)

    if params.categories is not None:
        query = query.where(ContestBase.categories == params.categories)

    return query


class ContestRepository:

    @staticmethod
    @transactional
    async def get_contest_by_id(contest_id: UUID, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        Contest: ContestBase | None = await session.get(
            ContestBase,
            contest_id,
        )
        return Contest

    @staticmethod
    @transactional
    async def add_contest(contest: ContestBase, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        session.add(contest)

    @staticmethod
    @transactional
    async def update_contest(contest: ContestBase, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        await session.merge(contest)

    @staticmethod
    @transactional
    async def get_all_contests(**kwargs: Any):
        session: AsyncSession = kwargs["session"]
        result = await session.execute(select(ContestBase))
        return result.scalars().all()

    @staticmethod
    @transactional
    async def get_contests(
        offset: int,
        per_page: int,
        params: ctrl.ContestQuery,
        is_approved: bool | None = None,
        **kwargs: Any,
    ):
        session: AsyncSession = kwargs["session"]
        query = select(ContestBase)

        if is_approved is not None:
            query = query.filter_by(is_approved=is_approved)

        query = await filters(query, params)

        query = query.offset(offset).limit(per_page)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    @transactional
    async def delete_contest(contest: ContestBase, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        await session.delete(contest)

    @staticmethod
    @transactional
    async def get_contest_by_column(
        column_name: str,
        value: Any,
        **kwargs: Any,
    ):
        session: AsyncSession = kwargs["session"]
        column = getattr(ContestBase, column_name, None)
        if column is None:
            raise ValueError(
                f"Column '{column_name}' does not exist in ContestBase.",
            )

        query = select(ContestBase).where(column == value)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    @transactional
    async def total_contests(
        params: ctrl.ContestQuery,
        is_approved: bool | None = None,
        **kwargs: Any,
    ) -> Any:

        session: AsyncSession = kwargs["session"]
        query = select(ContestBase)

        if is_approved is not None:
            query = query.filter_by(is_approved=is_approved)

        query = await filters(query, params)

        result = await session.execute(
            select(func.count()).select_from(query.subquery())
        )
        return result.scalar_one()
