import re
from pydantic import BaseModel, ConfigDict, field_validator
from app.models.user_model import UserRole


class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    role: str

    @field_validator("email")
    def email_must_be_valid(cls, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email address")
        return value

    @field_validator("role")
    def validate_role(cls, value):
        if value not in UserRole._value2member_map_:
            raise ValueError("Role must be 'ADMIN' or 'USER'")
        return value


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)
