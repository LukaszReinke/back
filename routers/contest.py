from uuid import UUID

import controllers as ctrl
import services as svc
from app_exceptions import errors
from authentication import PasswordManager, require_permissions
from core.enums import Permission as perm
from fastapi import APIRouter, Depends, Query, status
from models import UserBase

password_manager = PasswordManager()


router = APIRouter(prefix="/contests")


@router.post("/", response_model=ctrl.ContestResponse)
async def add_contest(new_contest: ctrl.ContestCreate):
    contest = await svc.ContestService.add_contest(new_contest)
    return contest


@router.get("/", response_model=ctrl.RawPaginatedContestResponse)
async def get_approved_contests(
    page: int = Query(1, ge=1), params: ctrl.ContestQuery = Depends()
):

    total_items = await svc.ContestService.total_contests(params, True)
    meta = ctrl.MetaData.create(page, total_items)

    if page > meta.total_pages:
        raise errors.PageOutOfRange

    contests = await svc.ContestService.get_contests(
        meta.offset, meta.page_size, params, True
    )

    return ctrl.RawPaginatedContestResponse(
        meta=meta,
        data=ctrl.RawContestDataResponse(
            items=[ctrl.RawContestResponse.model_validate(item) for item in contests],
            status="ok",
        ),
    )


@router.get("/all/", response_model=ctrl.PaginatedContestResponse)
async def get_all_contests(
    page: int = Query(1, ge=1),
    params: ctrl.ContestQuery = Depends(),
    is_approved: bool = Query(None),
    current_user: UserBase = Depends(require_permissions([perm.GET_CONTESTS])),
):

    total_items = await svc.ContestService.total_contests(params, is_approved)

    meta = ctrl.MetaData.create(page, total_items)

    if page > meta.total_pages:
        raise errors.PageOutOfRange

    contests = await svc.ContestService.get_contests(
        meta.offset, meta.page_size, params, is_approved
    )

    return ctrl.PaginatedContestResponse(
        meta=meta,
        data=ctrl.ContestDataResponse(
            items=[ctrl.ContestResponse.model_validate(item) for item in contests],
            status="ok",
        ),
    )


@router.get("/{contest_id}", response_model=ctrl.ContestResponse)
async def get_contest(contest_id: UUID):
    await svc.ContestService.get_contest(contest_id)


@router.put("/{contest_id}", status_code=status.HTTP_200_OK)
async def update_contest(
    contest_id: UUID,
    contest_update: ctrl.ContestUpdate,
    current_user: UserBase = Depends(require_permissions([perm.UPDATE_CONTEST])),
):
    await svc.ContestService.update_contest(contest_id, contest_update)


@router.delete("/{contest_id}", status_code=status.HTTP_200_OK)
async def delete_contest(
    contest_id: UUID,
    current_user: UserBase = Depends(require_permissions([perm.DELETE_CONTEST])),
):
    await svc.ContestService.delete_contest(contest_id)


@router.patch("/{contest_id}/approve", status_code=status.HTTP_200_OK)
async def approve_contest(
    contest_id: UUID,
    current_user: UserBase = Depends(require_permissions([perm.APPROVE_CONTEST])),
):
    await svc.ContestService.approve_contest(contest_id)
