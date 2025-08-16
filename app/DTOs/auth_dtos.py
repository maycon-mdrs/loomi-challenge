from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    role: str
    token: str
    

class Payload(BaseModel):
    id: str
    sub: str
    iat: int
    exp: int

    model_config = ConfigDict(from_attributes=True)
