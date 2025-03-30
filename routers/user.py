import controllers as ctrl
import services as svc

from app_exceptions import errors
from app_exceptions.exception_handler import generate_error_responses as responses

from authentication import require_permissions
from core.enums import Permission as perm
from fastapi import APIRouter, Depends, Query

router = APIRouter(prefix="/users")
router.responses = responses(errors.UserNotFound)


@router.post(
    "/", response_model=ctrl.UserResponse, responses=responses(errors.UserAlreadyExists)
)
async def add_user(
    new_user: ctrl.UserCreate,
    current_user: ctrl.RawUserResponse = Depends(require_permissions([perm.ADD_USER])),
):
    user = await svc.UserService.add_user(new_user, current_user)
    return user


@router.get("/", response_model=list[ctrl.UserResponse])
async def get_users(
    is_approved: bool = Query(None),
    current_user: ctrl.RawUserResponse = Depends(require_permissions([perm.GET_USERS])),
):
    users = await svc.UserService.get_users(is_approved)
    return users


@router.get("/{user_id}", response_model=ctrl.UserResponse)
async def get_user(
    user_id: int,
    current_user: ctrl.RawUserResponse = Depends(require_permissions([perm.GET_USERS])),
):
    user = await svc.UserService.get_user(user_id)
    return user


@router.delete("/{user_id}", response_model=ctrl.UserDelete)
async def delete_user(
    user_id: int,
    current_user: ctrl.RawUserResponse = Depends(
        require_permissions([perm.DELETE_USER])
    ),
):
    user = await svc.UserService.delete_user(user_id, current_user)
    return user


@router.post("/{user_id}/reset_password", response_model=ctrl.UserDelete)
async def reset_password(
    user_id: int,
    current_user: ctrl.RawUserResponse = Depends(
        require_permissions([perm.UPDATE_USER])
    ),
):
    # TO DO: send email
    user = await svc.UserService.get_user(user_id)
    return user


@router.put(
    "/{user_id}/update",
    response_model=ctrl.UserResponse,
    responses=responses(errors.RoleNotFound),
)
async def update_user(
    user_id: int,
    _user: ctrl.UserUpdate,
    current_user: ctrl.RawUserResponse = Depends(
        require_permissions([perm.UPDATE_USER])
    ),
):
    user = await svc.UserService.update_user(user_id, _user, current_user)
    return user
