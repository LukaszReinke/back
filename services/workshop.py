from typing import Any
from uuid import UUID

from app_exceptions import errors
import controllers as ctrl
import repositories as rp
from models import WorkshopBase


class WorkshopService:

    @staticmethod
    async def total_workshops(
        params: ctrl.WorkshopQuery, is_approved: bool | None = None
    ) -> Any:
        return await rp.WorkshopRepository.total_workshops(params, is_approved)

    @staticmethod
    async def add_workshop(_workshop: ctrl.WorkshopCreate):

        workshop = WorkshopBase(
            workshop_url=_workshop.workshop_url,
            workshop_topic=_workshop.workshop_topic,
            coaches=_workshop.coaches,
            organizer=_workshop.organizer,
            localization=_workshop.localization,
            start_date=_workshop.start_date,
            end_date=_workshop.end_date,
            categories=_workshop.categories,
            price=_workshop.price,
            contact=_workshop.contact,
            thumbnail_url=_workshop.thumbnail_url,
        )

        await rp.WorkshopRepository.add_workshop(workshop)

        return workshop

    @staticmethod
    async def delete_workshop(worhshop_id: UUID):
        workshop = await rp.WorkshopRepository.get_workshop_by_id(worhshop_id)

        if workshop is None:
            raise errors.WorkshopNotFound

        await rp.WorkshopRepository.delete_workshop(workshop)

    @staticmethod
    async def get_workshop(worhshop_id: UUID):
        workshop = await rp.WorkshopRepository.get_workshop_by_id(worhshop_id)
        if not isinstance(workshop, WorkshopBase):
            raise errors.WorkshopNotFound

        return workshop

    @staticmethod
    async def get_workshops(
        offset: int,
        per_page: int,
        params: ctrl.WorkshopQuery,
        is_approved: bool | None = None,
    ):
        return await rp.WorkshopRepository.get_workshops(
            offset, per_page, params, is_approved
        )

    @staticmethod
    async def update_workshop(worhshop_id: UUID, _workshop: ctrl.WorkshopUpdate):
        workshop = await rp.WorkshopRepository.get_workshop_by_id(worhshop_id)

        if not isinstance(workshop, WorkshopBase):
            raise errors.WorkshopNotFound

        for key, value in _workshop.model_dump(exclude_unset=True).items():
            setattr(workshop, key, value)

        await rp.WorkshopRepository.update_workshop(workshop)

        return workshop

    @staticmethod
    async def approve_workshop(worhshop_id: UUID):
        workshop: WorkshopBase = await rp.WorkshopRepository.get_workshop_by_id(
            worhshop_id
        )

        if workshop is None:
            raise errors.WorkshopNotFound
        if workshop.is_approved is True:
            raise errors.WorkshopArleadyApproved

        workshop.approve_workshop()

        await rp.UserRepository.update_user(workshop)
        return workshop
