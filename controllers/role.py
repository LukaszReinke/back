from pydantic import BaseModel
from datetime import datetime


class RoleResponse(BaseModel):
    role_id: int
    role_name: str
    level: int
    created_at: datetime


class RawRoleResponse(BaseModel):
    role_id: int
    role_name: str
    level: int

    model_config = {"from_attributes": True}


class RoleCreate(BaseModel):
    role_name: str
    level: int


class RoleUpdate(BaseModel):
    role_name: str | None
    description: str | None


class RoleDelete(BaseModel):
    role_id: int
    role_name: str


class ApproveRole(BaseModel):
    role_id: int
    role_name: str
