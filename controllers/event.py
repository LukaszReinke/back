from pydantic import BaseModel
from datetime import datetime


class EventResponse(BaseModel):
    event_id: int
    name: str
    category: str
    description: str
    date: datetime
    localization: str
    created_at: datetime
    is_approved: bool


class EventCreate(BaseModel):
    name: str
    category: str
    organizer_name: str
    description: str
    date: datetime
    localization: str


class EventUpdate(BaseModel):
    name: str | None
    category: str | None
    description: str | None
    date: datetime | None
    localization: str | None
    is_approved: bool | None


class EventDelete(BaseModel):
    event_id: int
    name: str


class ApproveEvent(BaseModel):
    event_id: int
    name: str
