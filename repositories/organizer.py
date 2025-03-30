from typing import Any

from models import OrganizerBase
from models.base import AsyncSession, transactional  # type: ignore
from sqlalchemy.future import select


class OrganizerRepository:

    @staticmethod
    @transactional
    async def get_organizer_by_id(organizer_id: int, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        organizer: OrganizerBase | None = await session.get(
            OrganizerBase,
            organizer_id,
        )
        return organizer

    @staticmethod
    @transactional
    async def get_organizer_by_name(name: str, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        query = select(OrganizerBase).where(OrganizerBase.name == name)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    @transactional
    async def get_organizer_by_email(email: str, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        query = select(OrganizerBase).where(OrganizerBase.email == email)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    @transactional
    async def add_organizer(organizer: OrganizerBase, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        session.add(organizer)

    @staticmethod
    @transactional
    async def update_organizer(organizer: OrganizerBase, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        await session.merge(organizer)

    @staticmethod
    @transactional
    async def get_all_organizers(**kwargs: Any):
        session: AsyncSession = kwargs["session"]
        result = await session.execute(select(OrganizerBase))
        return result.scalars().all()

    @staticmethod
    @transactional
    async def delete_organizer(organizer: OrganizerBase, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        await session.delete(organizer)
