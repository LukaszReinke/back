import repositories as rp
import controllers as ctrl
from models import EventBase, OrganizerBase

from datetime import datetime
from app_exceptions import errors


class EventService:

    @staticmethod
    async def add_event(_event: ctrl.EventCreate):

        event = await rp.EventRepository.get_event_by_column("name", _event.name)
        organizer = await rp.OrganizerRepository.get_organizer_by_name(
            _event.organizer_name
        )

        if isinstance(event, EventBase):
            raise errors.EventAlreadyExists

        if not isinstance(organizer, OrganizerBase):
            raise errors.OrganizerNotFound

        event = EventBase(
            name=_event.name,
            category=_event.category,
            organizer_id=organizer.organizer_id,
            description=_event.description,
            date=_event.date,
            localization=_event.localization,
            created_at=datetime.now(),
        )

        await rp.EventRepository.add_event(event)

        return event

    @staticmethod
    async def delete_event(event_id: int):
        event = await rp.EventRepository.get_event_by_id(event_id)

        if event is None:
            raise errors.EventNotFound

        await rp.EventRepository.delete_event(event)

    @staticmethod
    async def get_event(event_id: int):
        event = await rp.EventRepository.get_event_by_id(event_id)
        if not isinstance(event, EventBase):
            raise errors.EventNotFound

        return event

    @staticmethod
    async def get_events(
        name: str | None = None,
        is_approved: bool | None = None,
        category: str | None = None,
    ):

        return await rp.EventRepository.get_events(name, is_approved, category)

    @staticmethod
    async def update_event(event_id: int, _event: ctrl.EventUpdate):
        event = await rp.EventRepository.get_event_by_id(event_id)

        if not isinstance(event, EventBase):
            raise errors.EventNotFound

        for key, value in _event.model_dump(exclude_unset=True).items():
            setattr(event, key, value)

        await rp.EventRepository.update_event(event)

        return event

    @staticmethod
    async def approve_event(event_id: int):
        event: EventBase = await rp.EventRepository.get_event_by_id(event_id)

        if event is None:
            raise errors.EventNotFound

        if event.is_approved is True:
            raise errors.EventArleadyApproved

        event.approve_event()

        await rp.UserRepository.update_user(event)
        return event
