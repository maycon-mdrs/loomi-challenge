from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    user_id: int = Field(..., ge=1, description="user_id is required")
    chat_id: str | None = Field(None, description="chat_id (optional for new sessions)")
    prompt: str = Field(..., min_length=1, description="prompt is required")
    
    
class ChatMessageResponse(BaseModel):
    user_id: int
    chat_id: str | None
    response: str
    context: list | None
    
    model_config = ConfigDict(from_attributes=True)
