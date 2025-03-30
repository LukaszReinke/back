import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, DateTime, String
from datetime import datetime
from models.base import Base


class WorkshopBase(Base):
    __tablename__ = "workshops"

    workshop_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workshop_url = Column(String(255), nullable=False)
    workshop_topic = Column(String(255), nullable=False)
    coaches = Column(String(255), nullable=False)
    organizer = Column(String(255), nullable=False)
    localization = Column(String(255), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    attendance_limitation = Column(String(255), nullable=False)
    categories = Column(String(64), nullable=True)
    price = Column(String(64), nullable=True)
    contact = Column(String(64), nullable=True)
    thumbnail_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    is_approved = Column(Boolean, default=False)

    def approve_workshop(self):
        self.is_approved = True
