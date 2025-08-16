from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import status
from app.database.connection import Session as CustomSession
from fastapi.security import OAuth2PasswordBearer
from app.models.user_model import UserModel
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def get_db_session():
    try: 
        session = CustomSession()
        yield session
    finally:
        session.close()
