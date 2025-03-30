import controllers as ctrl
import services as svc

from app_exceptions import errors
from authentication.jwt_manager import JWTManager

from core.enums import Permission, Role, RolePermissions
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 30

jwt_manager = JWTManager(
    secret_key=SECRET_KEY,
    algorithm=ALGORITHM,
    expire_hours=TOKEN_EXPIRE_HOURS,
)


async def get_token_details(token: str) -> tuple[str, str | None]:
    try:
        payload = jwt_manager.decode_token(token)
        email: str | None = payload.get("email", None)
        role: str | None = payload.get("role", None)

        if not email:
            raise errors.InvalidTokenError

    except ExpiredSignatureError:
        raise errors.ExpiredTokenError

    except JWTError:
        raise errors.TokenValidationError

    return email, role


async def get_current_user(token: str = Depends(oauth2_scheme)) -> ctrl.UserResponse:
    email, _ = await get_token_details(token)
    _user = await svc.UserService.get_user_by_email(email)
    user = ctrl.UserResponse.model_validate(_user)

    return user


def require_permissions(required_permissions: list[Permission]):
    async def permission_check(token: str = Depends(oauth2_scheme)):
        email, _role = await get_token_details(token)

        _user = await svc.UserService.get_user_by_email(email)
        if _user.is_initial_password is True:
            raise errors.AccountNotApproved

        if _role is None:
            raise errors.RoleNotFound()

        role: Role | None = RolePermissions.get_role(_role)
        if role is None:
            raise errors.RoleNotFound()

        if _role != str(_user.role):
            print(role, _user.role)
            raise errors.InsufficientPermission()

        if not role.has_permissions(required_permissions):
            raise errors.UserNotFound()

        return _user

    return permission_check
