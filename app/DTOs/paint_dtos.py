from pydantic import BaseModel, ConfigDict
from pydantic import field_validator


class PaintRegister(BaseModel):
    paint_name: str
    color: str
    surface_type: str
    environment: str
    finish_type: str
    features: str | None = None
    line: str | None = None

    @field_validator('environment')
    def validate_environment(cls, value):
        allowed = {'indoor', 'outdoor', 'both'}
        if value not in allowed:
            raise ValueError("Environment must be 'indoor', 'outdoor' or 'both'")
        return value


class PaintResponse(BaseModel):
    id: int
    paint_name: str
    color: str
    surface_type: str
    environment: str
    finish_type: str
    features: str | None = None
    line: str | None = None

    model_config = ConfigDict(from_attributes=True)
    
    
class PaintUpdate(BaseModel):
    paint_name: str | None = None
    color: str | None = None
    surface_type: str | None = None
    environment: str | None = None
    finish_type: str | None = None
    features: str | None = None
    line: str | None = None

    @field_validator('environment')
    def validate_environment(cls, value):
        if value is not None:
            allowed = {'indoor', 'outdoor', 'both'}
            if value not in allowed:
                raise ValueError("Environment must be 'indoor', 'outdoor' or 'both'")
        return value
