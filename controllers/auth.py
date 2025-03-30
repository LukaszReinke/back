from pydantic import BaseModel
from pydantic import EmailStr
from controllers.user import UserResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
    message: str | None = None
