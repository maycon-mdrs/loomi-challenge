from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum, func
from enum import Enum
from app.database.base import Base


class UserRole(Enum):
    admin = "ADMIN"
    user = "USER"


class UserModel(Base):
    __tablename__ = 'users'
    
    id = Column('id', Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = Column('first_name', String, nullable=False)
    last_name = Column('last_name', String, nullable=False)
    email = Column('email', String, nullable=False, unique=True)
    password = Column('password', String, nullable=False)
    
    created_at = Column('created_at', DateTime(), server_default=func.now())
    updated_at = Column('updated_at', DateTime(), onupdate=func.now())
    
    role = Column(SqlEnum(UserRole), nullable=False)
