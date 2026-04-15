from sqlalchemy.orm import Session
from app.models.chat_model import ChatSessionModel


class ChatRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_chat_sessions_by_chat_id(self, chat_id: str) -> list[ChatSessionModel]:
        return (
            self.db_session.query(ChatSessionModel)
            .filter_by(chat_id=chat_id)
            .order_by(ChatSessionModel.created_at)
            .all()
        )

    def save_chat_session(self, chat_session: ChatSessionModel) -> ChatSessionModel:
        self.db_session.add(chat_session)
        self.db_session.flush()
        self.db_session.commit()
        return chat_session

    def delete_chat_sessions_by_chat_id(self, chat_id: str):
        """Exclui todas as sessões de chat associadas a um chat_id específico."""
        self.db_session.query(ChatSessionModel).filter_by(chat_id=chat_id).delete()
        self.db_session.commit()
