from sqlalchemy.orm import Session
from app.models.user_model import UserModel


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all(self) -> list[UserModel]:
        return self.db_session.query(UserModel).all()
    
    def get_by_id(self, user_id: int) -> UserModel:
        return self.db_session.query(UserModel).filter(UserModel.id == user_id).first()
    
    def get_by_email(self, email: str):
        return self.db_session.query(UserModel).filter(UserModel.email == email).first()
    
    def create(self, user: UserModel) -> UserModel:
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user
    
    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if user:
            self.db_session.delete(user)
            self.db_session.commit()
            return True
        return False
