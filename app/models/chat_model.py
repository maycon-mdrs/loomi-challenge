from sqlalchemy import Column, Integer, String, DateTime, Text, func
from app.database.base import Base


class ChatSessionModel(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, index=True, nullable=True)
    user_id = Column(Integer, nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
