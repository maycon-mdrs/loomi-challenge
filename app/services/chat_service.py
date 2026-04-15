import uuid
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, AIMessage

from app.DTOs.chat_dtos import ChatMessageResponse, ChatRequest
from app.core_ai.agents.supervisor_workflow import get_supervisor_workflow
from app.models.chat_model import ChatSessionModel
from app.repositories.chat_repository import ChatRepository
from app.utils.logger import LoggerConfig

logger = LoggerConfig.get_logger(__name__)


class ChatService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.graph = get_supervisor_workflow()
        self.chat_repository = ChatRepository(db_session)

    def get_chat_history(self, session_id: str) -> list[ChatSessionModel]:
        """Retrieves the chat history stored in the database for the provided chat_id."""
        try:
            chat_sessions = self.chat_repository.get_chat_sessions_by_chat_id(session_id)
            chat_history = []
            for session in chat_sessions:
                chat_history.append(HumanMessage(content=session.prompt))
                chat_history.append(AIMessage(content=session.response))
            return chat_history
        except Exception:
            logger.error(f"Error retrieving chat history: {e}")
            return []

    def save_chat_session(self, session_id: str, question: str, answer: str, user_id: str) -> ChatSessionModel:
        """Saves the chat session history to the database."""
        try:
            chat_session = ChatSessionModel(
                chat_id=session_id,
                prompt=question,
                response=answer,
                user_id=user_id,
            )
            return self.chat_repository.save_chat_session(chat_session)
        except Exception as e:
            logger.error(f"Error saving chat session: {e}")

    def process_chat(self, query_input: ChatRequest, is_admin: bool = False) -> ChatMessageResponse:
        try:
            # If there is no session_id, create a new UUID
            session_id = query_input.chat_id if query_input.chat_id else str(uuid.uuid4())
            user_id = query_input.user_id

            chat_history = self.get_chat_history(session_id)
            
            # Adds the new user question
            chat_messages = chat_history + [HumanMessage(content=query_input.prompt)]

            # Pass user context (is_admin) to the graph via config
            result = self.graph.invoke(
                {"messages": chat_messages},
                config={"configurable": {"is_admin": is_admin}}
            )
            response = result["messages"][-1].content

            self.save_chat_session(session_id, query_input.prompt, response, user_id)

            return ChatMessageResponse(
                user_id=user_id,
                chat_id=session_id,
                response=response,
                context=result["messages"],
            )

        except Exception as e:
            logger.error(f"Error processing chat: {e}")
            return ChatMessageResponse(
                user_id=query_input.user_id,
                chat_id=query_input.chat_id,
                response="Ocorreu um erro ao processar sua solicitação.",
                context=[],
            )
