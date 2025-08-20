from fastapi import APIRouter, Depends, status
from requests import Session
from fastapi import APIRouter

from app.DTOs.chat_dtos import ChatMessageResponse, ChatRequest
from app.services.chat_service import ChatService
from app.utils.depends import get_db_session


chat_router = APIRouter(prefix='/chat', tags=['Chat'])


@chat_router.post(
    "/",
    status_code=status.HTTP_200_OK,
    description="""Endpoint de conversa com o assistente PintAI.\n\nFluxo de uso:\n- Primeira mensagem: envie `chat_id` como `null`. O backend irá criar uma nova sessão e retornar um `chat_id` único.\n- Continuação: utilize o `chat_id` retornado anteriormente para manter o contexto da conversa.\n\nExemplo de requisição:\n{\n  \"user_id\": 123,\n  \"chat_id\": null,\n  \"prompt\": \"Quero pintar meu quarto, mas prefiro algo que seja fácil de limpar e sem cheiro forte. Tem alguma sugestão?\"\n}\n\nO retorno segue o modelo:\n{\n  \"user_id\": 123,\n  \"chat_id\": \"<chat_id_retornado>\",\n  \"response\": \"...\",\n  \"context\": [ ... ]\n}\n""",
    response_model=ChatMessageResponse,
)
def chat_llm(chat_request: ChatRequest, db_session: Session = Depends(get_db_session)):
    chat_service = ChatService(db_session)
    return chat_service.process_chat(query_input=chat_request)
