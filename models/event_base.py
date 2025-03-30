from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base


class EventBase(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    category = Column(String(255), index=True)
    organizer_id = Column(
        Integer, ForeignKey("organizers.organizer_id"), nullable=False
    )
    description = Column(String(255), index=True)
    date = Column(DateTime, index=True)
    localization = Column(String(255), index=True)
    created_at = Column(DateTime, default=datetime.now)
    is_approved = Column(Boolean, default=False)

    organizer = relationship("OrganizerBase", back_populates="events")

    def approve_event(self):
        self.is_approved = True
