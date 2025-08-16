import uuid

from sqlalchemy import Column, String, DateTime, func
from app.database.base import Base
from enum import Enum, StrEnum
from sqlalchemy.dialects.postgresql import UUID    


class UserRole(Enum):
    admin = "ADMIN"
    user = "USER"


class UserModel(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    first_name = Column('first_name', String, nullable=False)
    last_name = Column('last_name', String, nullable=False)
    email = Column('email', String, nullable=False, unique=True)
    password = Column('password', String, nullable=False)
    
    created_at = Column('created_at', DateTime(), server_default=func.now())
    updated_at = Column('updated_at', DateTime(), server_default=func.now(), onupdate=func.now())
    
    role = Column(StrEnum(UserRole), nullable=False)
