from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.connection import Session as CustomSession
from fastapi.security import OAuth2PasswordBearer
from app.exceptions.auth_exceptions import AdminAccessRequiredException
from app.models.user_model import UserModel, UserRole
from app.services.auth_service import AuthService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db_session():
    try:
        session = CustomSession()
        yield session
    finally:
        session.close()


def get_current_user(db_session: Session = Depends(get_db_session), token=Depends(oauth2_scheme)):
    auth_service = AuthService(db_session=db_session)
    return auth_service.verify_token(token)


def admin_required(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    if current_user.role != UserRole.ADMIN:
        raise AdminAccessRequiredException()
    return current_user
