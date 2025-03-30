import controllers as ctrl
import services as svc

from app_exceptions import errors
from app_exceptions.exception_handler import generate_error_responses as responses

from authentication import require_permissions
from core.enums import Permission as perm
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/organizers")
router.responses = responses(errors.OrganizerAlreadyExists, errors.OrganizerNotFound)


@router.post("/", response_model=ctrl.OrganizerResponse)
async def add_organizer(
    new_organizer: ctrl.OrganizerCreate,
    current_user: ctrl.RawUserResponse = Depends(
        require_permissions([perm.ADD_ORGANIZER])
    ),
):
    organizer = await svc.OrganizerService.add_organizer(new_organizer)
    return organizer


@router.get("/", response_model=list[ctrl.OrganizerResponse])
async def get_organizers():
    organizers = await svc.OrganizerService.get_organizers()
    return organizers


@router.get("/{organizer_id}", response_model=ctrl.OrganizerResponse)
async def get_organizer(
    organizer_id: int,
    current_user: ctrl.RawUserResponse = Depends(
        require_permissions([perm.GET_ORGANIZERS])
    ),
):
    organizer = await svc.OrganizerService.get_organizer(organizer_id)
    return organizer


@router.delete("/{organizer_id}", response_model=ctrl.OrganizerDelete)
async def delete_organizer(
    organizer_id: int,
    current_user: ctrl.RawUserResponse = Depends(
        require_permissions([perm.DELETE_ORGANIZER])
    ),
):
    organizer = await svc.OrganizerService.delete_organizer(organizer_id)
    return organizer


@router.put("/{organizer_id}", response_model=ctrl.OrganizerResponse)
async def update_organizer(
    organizer_id: int,
    organizer_update: ctrl.OrganizerUpdate,
    current_user: ctrl.RawUserResponse = Depends(
        require_permissions([perm.UPDATE_ORGANIZER])
    ),
):
    await svc.OrganizerService.update_organizer(organizer_id, organizer_update)
