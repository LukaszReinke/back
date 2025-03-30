import controllers as ctrl
import services as svc

from app_exceptions import errors
from app_exceptions.exception_handler import generate_error_responses as responses
from authentication import require_permissions

from core.enums import EventCategory
from core.enums import Permission as perm
from fastapi import APIRouter, Depends, Query

router = APIRouter(prefix="/events")
router.responses = responses(errors.EventNotFound, errors.EventAlreadyExists)


@router.post("/", response_model=ctrl.EventResponse)
async def add_event(
    new_event: ctrl.EventCreate,
    current_user: ctrl.RawUserResponse = Depends(require_permissions([perm.ADD_EVENT])),
):
    event = await svc.EventService.add_event(new_event)
    return event


@router.get("/", response_model=list[ctrl.EventResponse])
async def get_approved_events(
    name: str = Query(None),
    category: EventCategory | None = Query(default=None),
):

    events = await svc.EventService.get_events(name, True, category)
    return events


@router.get("/all/", response_model=list[ctrl.EventResponse])
async def get_all_events(
    name: str = Query(None),
    category: EventCategory = Query(None),
    is_approved: bool = Query(None),
    current_user: ctrl.RawUserResponse = Depends(
        require_permissions([perm.GET_EVENTS])
    ),
):

    events = await svc.EventService.get_events(name, is_approved, category)
    return events


@router.get("/{event_id}", response_model=ctrl.EventResponse)
async def get_event(event_id: int):
    await svc.EventService.get_event(event_id)


@router.put("/{event_id}", response_model=ctrl.EventResponse)
async def update_event(
    event_id: int,
    event_update: ctrl.EventUpdate,
    current_user: ctrl.RawUserResponse = Depends(
        require_permissions([perm.UPDATE_EVENT])
    ),
):
    await svc.EventService.update_event(event_id, event_update)


@router.delete("/{event_id}", response_model=ctrl.EventDelete)
async def delete_event(
    event_id: int,
    current_user: ctrl.RawUserResponse = Depends(
        require_permissions([perm.DELETE_EVENT])
    ),
):
    await svc.EventService.delete_event(event_id)


@router.patch("/{event_id}/approve", response_model=ctrl.EventResponse)
async def approve_event(
    event_id: int,
    current_user: ctrl.RawUserResponse = Depends(
        require_permissions([perm.APPROVE_EVENT])
    ),
):
    await svc.EventService.approve_event(event_id)
