import controllers as ctrl
import repositories as rp
from authentication import PasswordManager
from models import OrganizerBase
from app_exceptions import errors

password_manager = PasswordManager()


class OrganizerService:

    @staticmethod
    async def add_organizer(_organizer: ctrl.OrganizerCreate):
        check_organizer = await rp.OrganizerRepository.get_organizer_by_name(
            _organizer.name
        )
        if isinstance(check_organizer, OrganizerBase):
            raise errors.OrganizerNotFound

        check_organizer = await rp.OrganizerRepository.get_organizer_by_email(
            _organizer.email
        )
        if isinstance(check_organizer, OrganizerBase):
            raise errors.OrganizerAlreadyExists

        organizer = OrganizerBase(
            name=_organizer.name,
            email=_organizer.email,
            description=_organizer.description,
            logo_url=_organizer.logo_url,
            website_url=_organizer.website_url,
            phone_number=_organizer.phone_number,
            address=_organizer.address,
        )

        await rp.OrganizerRepository.add_organizer(organizer)

        return organizer

    @staticmethod
    async def delete_organizer(organizer_id: int):
        organizer = await rp.OrganizerRepository.get_organizer_by_id(organizer_id)

        if organizer is None:
            raise errors.OrganizerNotFound

        await rp.OrganizerRepository.delete_organizer(organizer)

    @staticmethod
    async def get_organizer(organizer_id: int):
        organizer = await rp.OrganizerRepository.get_organizer_by_id(organizer_id)

        if organizer is None:
            raise errors.OrganizerNotFound

        return organizer

    @staticmethod
    async def get_organizers():
        organizers = await rp.OrganizerRepository.get_all_organizers()
        return organizers

    @staticmethod
    async def update_organizer(organizer_id: int, _organizer: ctrl.OrganizerUpdate):
        organizer = await rp.OrganizerRepository.get_organizer_by_id(organizer_id)

        if not isinstance(organizer, OrganizerBase):
            raise errors.OrganizerNotFound

        for key, value in _organizer.model_dump(exclude_unset=True).items():
            setattr(organizer, key, value)

        await rp.OrganizerRepository.update_organizer(organizer)

        return organizer
