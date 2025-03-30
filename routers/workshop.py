from uuid import UUID

import controllers as ctrl
import services as svc
from app_exceptions import errors
from authentication import PasswordManager, require_permissions
from core.enums import Permission as perm
from fastapi import APIRouter, Depends, Query
from models import UserBase

password_manager = PasswordManager()


router = APIRouter(prefix="/workshops")


@router.post("/", response_model=ctrl.WorkshopResponse)
async def add_workshop(new_workshop: ctrl.WorkshopCreate):
    workshop = await svc.WorkshopService.add_workshop(new_workshop)
    return workshop


@router.get("/", response_model=ctrl.RawPaginatedWorkshopResponse)
async def get_approved_workshops(
    page: int = Query(1, ge=1),
    params: ctrl.WorkshopQuery = Depends(),
):
    total_items = await svc.WorkshopService.total_workshops(params, True)
    meta = ctrl.MetaData.create(page, total_items)

    if page > meta.total_pages:
        raise errors.PageOutOfRange

    workshops = await svc.WorkshopService.get_workshops(
        meta.offset, meta.page_size, params, True
    )

    return ctrl.RawPaginatedWorkshopResponse(
        meta=meta,
        data=ctrl.RawWorkshopDataResponse(
            items=[ctrl.RawWorkshopResponse.model_validate(item) for item in workshops],
            status="ok",
        ),
    )


@router.get("/all/", response_model=ctrl.PaginatedWorkshopResponse)
async def get_all_workshops(
    page: int = Query(1, ge=1),
    params: ctrl.WorkshopQuery = Depends(),
    is_approved: bool | None = Query(None),
    current_user: UserBase = Depends(require_permissions([perm.GET_WORKSHOPS])),
):

    total_items = await svc.WorkshopService.total_workshops(params, is_approved)
    meta = ctrl.MetaData.create(page, total_items)

    if page > meta.total_pages:
        raise errors.PageOutOfRange

    workshops = await svc.WorkshopService.get_workshops(
        meta.offset, meta.page_size, params, is_approved
    )
    return ctrl.PaginatedWorkshopResponse(
        meta=meta,
        data=ctrl.WorkshopDataResponse(
            items=[ctrl.WorkshopResponse.model_validate(item) for item in workshops],
            status="ok",
        ),
    )


@router.get("/{workshop_id}", response_model=ctrl.WorkshopResponse)
async def get_workshop(workshop_id: UUID):
    await svc.WorkshopService.get_workshop(workshop_id)


@router.put("/{workshop_id}", response_model=ctrl.WorkshopResponse)
async def update_workshop(
    workshop_id: UUID,
    workshop_update: ctrl.WorkshopUpdate,
    current_user: UserBase = Depends(require_permissions([perm.UPDATE_WORKSHOP])),
):
    await svc.WorkshopService.update_workshop(workshop_id, workshop_update)


@router.delete("/{workshop_id}", response_model=ctrl.WorkshopDelete)
async def delete_workshop(
    workshop_id: UUID,
    current_user: UserBase = Depends(require_permissions([perm.DELETE_WORKSHOP])),
):
    await svc.WorkshopService.delete_workshop(workshop_id)


@router.patch("/{workshop_id}/approve", response_model=ctrl.WorkshopResponse)
async def approve_workshop(
    workshop_id: UUID,
    current_user: UserBase = Depends(require_permissions([perm.APPROVE_WORKSHOP])),
):
    await svc.WorkshopService.approve_workshop(workshop_id)
