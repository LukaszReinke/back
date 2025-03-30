from datetime import datetime
from uuid import UUID

from controllers.meta import MetaData
from pydantic import BaseModel, Field


class ContestResponse(BaseModel):
    contest_id: UUID
    contest_url: str
    contest_name: str
    localization: str
    start_date: datetime
    end_date: datetime | None
    categories: str | None
    contact: str | None
    thumbnail_url: str | None
    created_at: datetime
    is_approved: bool

    model_config = {"from_attributes": True}


class ContestQuery(BaseModel):
    contest_name: str | None = Field(None)
    localization: str | None = Field(None)
    start_date: datetime | None = Field(None)
    end_date: datetime | None = Field(None)
    categories: str | None = Field(None)


class ContestDataResponse(BaseModel):
    status: str
    items: list[ContestResponse]


class PaginatedContestResponse(BaseModel):
    meta: MetaData
    data: ContestDataResponse


class RawContestResponse(BaseModel):
    contest_id: UUID
    contest_url: str
    contest_name: str
    localization: str
    start_date: datetime
    end_date: datetime | None
    categories: str | None
    contact: str | None
    thumbnail_url: str | None

    model_config = {"from_attributes": True}


class RawContestDataResponse(BaseModel):
    status: str
    items: list[RawContestResponse]


class RawPaginatedContestResponse(BaseModel):
    meta: MetaData
    data: RawContestDataResponse


class ContestCreate(BaseModel):
    contest_url: str
    contest_name: str
    localization: str
    start_date: datetime
    end_date: datetime | None = None
    categories: str | None = None
    contact: str | None = None
    thumbnail_url: str | None = None


class ContestUpdate(BaseModel):
    contest_url: str | None
    contest_name: str | None
    localization: str | None
    start_date: datetime | None
    end_date: datetime | None
    categories: str | None
    contact: str | None
    thumbnail_url: str | None
    created_at: datetime | None
    is_approved: bool | None


class ContestDelete(BaseModel):
    contest_id: UUID
    contest_url: str
    contest_name: str
