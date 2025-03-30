import controllers as ctrl
import services as svc

from authentication import PasswordManager, get_current_user
from app_exceptions.exception_handler import generate_error_responses as responses

from fastapi import APIRouter, Depends

password_manager = PasswordManager()


router = APIRouter(prefix="/profile")
router.responses = responses()


@router.get("/", response_model=ctrl.UserResponse)
async def me(current_user: ctrl.UserResponse = Depends(get_current_user)):
    return current_user


@router.put("/", response_model=ctrl.UserResponse)
async def edit_profile(
    _profile: ctrl.ProfileUpdateRequest,
    current_user: ctrl.UserResponse = Depends(get_current_user),
):
    user = await svc.UserService.update_profile(_profile, current_user)
    return user
