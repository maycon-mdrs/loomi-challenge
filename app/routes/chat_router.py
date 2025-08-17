from fastapi import APIRouter, Depends, status
from requests import Session
from fastapi import APIRouter

from app.DTOs.chat_dtos import ChatRequest
from app.services.chat_service import ChatService
from app.utils.depends import get_db_session


chat_router = APIRouter(prefix='/chat', tags=['Chat'])


@chat_router.post("/", status_code=status.HTTP_200_OK)
def chat_llm(chat_request: ChatRequest, db_session: Session = Depends(get_db_session)):
    chat_service = ChatService(db_session)
    return chat_service.process_chat(query_input=chat_request)
