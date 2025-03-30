import controllers as ctrl
import repositories as rp

from authentication import (
    PasswordManager,
)

from fastapi import HTTPException, status

from models import UserBase
from app_exceptions import errors
from core.enums import RolePermissions, Role

password_manager = PasswordManager()


class UserService:

    @staticmethod
    async def add_user(_user: ctrl.UserCreate, current_user: ctrl.RawUserResponse):
        _role: Role = RolePermissions.get_role(str(_user.role))
        current_user_role: Role = RolePermissions.get_role(str(current_user.role))

        if int(current_user_role.level) >= int(_role.level):  # type: ignore
            raise errors.InsufficientPermission

        check_user = await rp.UserRepository.get_user_by_email(_user.email)
        if isinstance(check_user, UserBase):
            raise errors.UserAlreadyExists

        initial_password = password_manager.generate_password()
        hashed_password = password_manager.hash_password(initial_password)

        user = UserBase(
            email=_user.email,
            first_name=_user.first_name,
            last_name=_user.last_name,
            phone_number=_user.phone_number,
            role=_user.role,
            hashed_password=hashed_password,
        )

        await rp.UserRepository.add_user(user)

        return user

    @staticmethod
    async def delete_user(user_id: int, current_user: ctrl.RawUserResponse):
        _user = await rp.UserRepository.get_user_by_id(user_id)
        if _user is None:
            raise errors.UserNotFound

        _role: Role = _user.get_role()
        current_user_role: Role = RolePermissions.get_role(str(current_user.role))

        if int(current_user_role.level) >= int(_role.level):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permitted access",
            )

        await rp.UserRepository.delete_user(_user)
        return _user

    @staticmethod
    async def get_user(user_id: int):
        user = await rp.UserRepository.get_user_by_id(user_id)

        if user is None:
            raise errors.UserNotFound

        return user

    @staticmethod
    async def get_user_by_email(email: str):
        user = await rp.UserRepository.get_user_by_email(email)

        if user is None:
            raise errors.UserNotFound

        return user

    @staticmethod
    async def get_users(
        is_approved: bool | None = None,
    ):
        users = await rp.UserRepository.get_users(is_approved)
        return users

    @staticmethod
    async def update_user(
        user_id: int, _change: ctrl.UserUpdate, current_user: ctrl.RawUserResponse
    ) -> UserBase:
        _user = await rp.UserRepository.get_user_by_id(user_id)
        if _user is None:
            raise errors.UserNotFound

        _role: Role = _user.get_role()
        _change_role = RolePermissions.get_role(str(_change.role))
        current_user_role: Role = RolePermissions.get_role(str(current_user.role))

        if _change_role is None:
            raise errors.RoleNotFound

        if _role.level >= current_user_role.level >= _change_role.level:
            raise errors.InsufficientPermission

        for key, value in _change.model_dump(exclude_unset=True).items():
            setattr(_user, key, value)

        user = await rp.UserRepository.update_user(_user)

        return user

    @staticmethod
    async def update_profile(
        _change: ctrl.ProfileUpdateRequest, current_user: ctrl.UserResponse
    ):
        _user = await rp.UserRepository.get_user_by_id(current_user.user_id)

        if not password_manager.verify_password(
            _change.password, str(_user.hashed_password)  # type: ignore
        ):
            raise errors.InvalidCredentials

        _change.__setattr__("password", None)

        if _change.new_password is not None:
            hashed_password = password_manager.hash_password(_change.new_password)
            setattr(_user, "hashed_password", hashed_password)

        for key, value in _change.model_dump(exclude_unset=True).items():
            setattr(_user, key, value)

        print(_user.__dict__)
        await rp.UserRepository.update_user(_user)

        return _user
