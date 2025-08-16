from sqlalchemy.orm import Session
from passlib.context import CryptContext
from decouple import config            

from app.DTOs.user_dtos import UserRegister
from app.exceptions.user_exceptions import UserAlreadyExistsException, UserCreationException, UserNotFoundException
from app.models.user_model import UserModel, UserRole
from app.repositories.user_repository import UserRepository

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
crypt_context = CryptContext(schemes=["sha256_crypt"])

class UserService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.user_repository = UserRepository(db_session)

    def register_user(self, user: UserRegister) -> UserModel:        
        existing_user = self._get_user_by_email(user.email)
        if existing_user:
            raise UserAlreadyExistsException()
        
        user = UserModel(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=crypt_context.hash(user.password),
            role=UserRole(user.role)
        )
        
        try:
            return self.user_repository.create(user)
        except Exception:
            raise UserCreationException()
        
    def _get_user_by_email(self, email: str) -> UserModel:
        return self.user_repository.get_by_email(email)
    
    def get_user_by_email(self, email: str) -> UserModel:
        user = self._get_user_by_email(email)
        if not user:
            raise UserNotFoundException()
        return user

    def get_user_by_id(self, user_id: int) -> UserModel:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        return user
    
    def get_all_users(self) -> list[UserModel]:
        return self.user_repository.get_all()    
    
    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        return self.user_repository.delete(user.id)
