from models.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class OrganizerBase(Base):
    __tablename__ = "organizers"

    organizer_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        index=True,
    )
    name = Column(String(128), nullable=False, unique=True, index=True)
    email = Column(String(128), nullable=False, unique=True, index=True)
    description = Column(String(255), index=True)
    logo_url = Column(String(255))
    website_url = Column(String(255))
    phone_number = Column(String(12), unique=True, index=True)
    address = Column(String(255))

    events = relationship("EventBase", back_populates="organizer")
