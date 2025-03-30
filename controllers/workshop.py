from datetime import datetime
from uuid import UUID

from controllers.meta import MetaData
from pydantic import BaseModel, Field


class WorkshopResponse(BaseModel):
    workshop_id: UUID
    workshop_url: str
    workshop_topic: str
    coaches: str
    organizer: str
    localization: str
    start_date: datetime
    end_date: datetime | None
    attendance_limitation: str | None
    categories: str | None
    price: str | None
    contact: str | None
    thumbnail_url: str | None
    created_at: datetime
    is_approved: bool

    model_config = {"from_attributes": True}


class WorkshopQuery(BaseModel):
    workshop_topic: str | None = Field(None)
    coaches: str | None = Field(None)
    organizer: str | None = Field(None)
    localization: str | None = Field(None)
    start_date: datetime | None = Field(None)
    end_date: datetime | None = Field(None)
    attendance_limitation: str | None = Field(None)
    categories: str | None = Field(None)
    price: str | None = Field(None)


class WorkshopDataResponse(BaseModel):
    status: str
    items: list[WorkshopResponse]


class PaginatedWorkshopResponse(BaseModel):
    meta: MetaData
    data: WorkshopDataResponse


class RawWorkshopResponse(BaseModel):
    workshop_id: UUID
    workshop_url: str
    workshop_topic: str
    coaches: str
    organizer: str
    localization: str
    start_date: datetime
    end_date: datetime | None
    attendance_limitation: str | None
    thumbnail_url: str | None

    model_config = {"from_attributes": True}


class RawWorkshopDataResponse(BaseModel):
    status: str
    items: list[RawWorkshopResponse]


class RawPaginatedWorkshopResponse(BaseModel):
    meta: MetaData
    data: RawWorkshopDataResponse


class WorkshopCreate(BaseModel):
    workshop_url: str
    workshop_topic: str
    coaches: str
    organizer: str
    localization: str
    start_date: datetime
    end_date: datetime | None = None
    attendance_limitation: str | None = None
    categories: str | None = None
    price: str | None = None
    contact: str | None = None
    thumbnail_url: str | None = None


class WorkshopUpdate(BaseModel):
    worskop_url: str | None
    coaches: str | None
    workshop_topic: str | None
    organizer: str | None
    localization: str | None
    start_date: datetime | None
    end_date: datetime | None
    attendance_limitation: str | None
    categories: str | None
    price: str | None
    contact: str | None
    thumbnail_url: str | None
    is_approved: bool | None


class WorkshopDelete(BaseModel):
    worskop_id: UUID
    worskop_url: str
    workshop_name: str
