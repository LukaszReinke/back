from models.base import Base
from sqlalchemy import Column, Integer, String, Boolean
from core.enums import RolePermissions, Role


class UserBase(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(64), unique=True, index=True)
    first_name = Column(String(64))
    last_name = Column(String(64))
    phone_number = Column(String(64), nullable=True)
    hashed_password = Column(String)
    role = Column(String(64))
    is_initial_password = Column(Boolean, default=True)

    def change_password(self, new_hashed_password: str):
        self.hashed_password = new_hashed_password
        self.is_initial_password = False

    def get_role(self) -> Role:
        return RolePermissions.get_role(str(self.role))
