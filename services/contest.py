from typing import Any
import repositories as rp
import controllers as ctrl
from models import ContestBase
from uuid import UUID

from app_exceptions import errors


class ContestService:

    @staticmethod
    async def total_contests(
        params: ctrl.ContestQuery, is_approved: bool | None = None
    ) -> Any:
        return await rp.ContestRepository.total_contests(params, is_approved)

    @staticmethod
    async def add_contest(_contest: ctrl.ContestCreate):

        contest = await rp.ContestRepository.get_contest_by_column(
            "contest_name", _contest.contest_name
        )

        contest = ContestBase(
            contest_url=_contest.contest_url,
            contest_name=_contest.contest_name,
            localization=_contest.localization,
            start_at=_contest.start_at,
            end_at=_contest.end_at,
            categories=_contest.categories,
            contact=_contest.contact,
            thumbnail_url=_contest.thumbnail_url,
        )

        await rp.ContestRepository.add_contest(contest)

        return contest

    @staticmethod
    async def delete_contest(contest_id: UUID):
        contest = await rp.ContestRepository.get_contest_by_id(contest_id)

        if contest is None:
            raise errors.ContestNotFound

        await rp.ContestRepository.delete_contest(contest)

    @staticmethod
    async def get_contest(contest_id: UUID):
        contest = await rp.ContestRepository.get_contest_by_id(contest_id)
        if not isinstance(contest, ContestBase):
            raise errors.ContestNotFound

        return contest

    @staticmethod
    async def get_contests(
        offset: int,
        per_page: int,
        params: ctrl.ContestQuery,
        is_approved: bool | None = None,
    ):

        return await rp.ContestRepository.get_contests(
            offset, per_page, params, is_approved
        )

    @staticmethod
    async def update_contest(contest_id: UUID, _contest: ctrl.ContestUpdate):
        contest = await rp.ContestRepository.get_contest_by_id(contest_id)

        if not isinstance(contest, ContestBase):
            raise errors.ContestNotFound

        for key, value in _contest.model_dump(exclude_unset=True).items():
            setattr(contest, key, value)

        await rp.ContestRepository.update_contest(contest)

        return contest

    @staticmethod
    async def approve_contest(contest_id: UUID):
        contest: ContestBase = await rp.ContestRepository.get_contest_by_id(contest_id)

        if contest is None:
            raise errors.ContestNotFound

        if contest.is_approved is True:
            raise errors.ContestArleadyApproved

        contest.approve_contest()

        await rp.UserRepository.update_user(contest)
        return contest
