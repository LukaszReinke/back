import uuid
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from models.base import Base


class ContestBase(Base):
    __tablename__ = "contests"

    contest_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contest_url = Column(String(255), nullable=False)
    contest_name = Column(String(255), nullable=False)
    localization = Column(String(255), index=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    categories = Column(String(255), nullable=True)
    contact = Column(String(64), nullable=True)
    thumbnail_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    is_approved = Column(Boolean, default=False)

    def approve_contest(self):
        self.is_approved = True
