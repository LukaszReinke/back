from typing import Any
from sqlalchemy.future import select
from models import UserBase
from models.base import AsyncSession, transactional  # type: ignore


class UserRepository:

    @staticmethod
    @transactional
    async def get_user_by_id(user_id: int, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        user: UserBase | None = await session.get(
            UserBase,
            user_id,
        )
        return user

    @staticmethod
    @transactional
    async def add_user(user: UserBase, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        session.add(user)

    @staticmethod
    @transactional
    async def update_user(user: UserBase, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        await session.merge(user)
        return user

    @staticmethod
    @transactional
    async def get_users(
        is_approved: bool | None = None,
        **kwargs: Any,
    ):
        session: AsyncSession = kwargs["session"]
        query = select(UserBase)

        if is_approved is not None:
            query = query.filter_by(is_approved=is_approved)

        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    @transactional
    async def delete_user(user: UserBase, **kwargs: Any):
        session: AsyncSession = kwargs["session"]
        await session.delete(user)

    @staticmethod
    @transactional
    async def get_user_by_email(email: str, **kwargs: Any) -> UserBase | None:
        session: AsyncSession = kwargs["session"]
        query = select(UserBase).where(UserBase.email == email)
        result = await session.execute(query)
        return result.scalars().first()
