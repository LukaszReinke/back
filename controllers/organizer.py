from pydantic import BaseModel, EmailStr


class OrganizerResponse(BaseModel):
    organizer_id: int
    name: str
    email: EmailStr
    description: str | None
    logo_url: str | None
    website_url: str | None
    phone_number: str | None
    address: str | None


class RawOrganizerResponse(BaseModel):
    organizer_id: int
    name: str
    email: EmailStr


class OrganizerCreate(BaseModel):
    name: str
    email: EmailStr
    description: str | None
    logo_url: str | None
    website_url: str | None
    phone_number: str | None
    address: str | None


class OrganizerUpdate(BaseModel):
    name: str | None
    email: EmailStr | None
    description: str | None
    logo_url: str | None
    website_url: str | None
    phone_number: str | None
    address: str | None


class OrganizerDelete(BaseModel):
    organizer_id: int
    name: str
