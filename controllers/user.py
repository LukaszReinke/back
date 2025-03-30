from pydantic import BaseModel
from pydantic import EmailStr
from core.enums import UserRole


class UserResponse(BaseModel):
    user_id: int
    email: str
    role: UserRole
    first_name: str
    last_name: str
    phone_number: str | None
    is_initial_password: bool

    model_config = {"from_attributes": True}


class RawUserResponse(BaseModel):
    user_id: int
    role: UserRole
    first_name: str
    last_name: str
    phone_number: str

    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str | None = None
    role: UserRole

    class Config:
        use_enum_values = True


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    role: UserRole | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None

    class Config:
        use_enum_values = True


class ProfileUpdateRequest(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    password: str
    new_password: str | None = None


class ProfileResponse(BaseModel):
    first_name: str
    last_name: str
    phone_number: str | None


class UserChangeRole(BaseModel):
    user_id: int
    role: UserRole

    class Config:
        use_enum_values = True


class UserDelete(BaseModel):
    user_id: int
    email: str


class ApproveUser(BaseModel):
    user_id: int
    email: str
