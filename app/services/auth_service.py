from datetime import datetime, timedelta
from app.DTOs.auth_dtos import LoginResponse, Payload
from sqlalchemy.orm import Session
from app.config import SECRET_KEY, ALGORITHM, crypt_context
from jose import ExpiredSignatureError, jwt, JWTError

from app.DTOs.auth_dtos import LoginRequest
from app.exceptions.auth_exceptions import InvalidCredentialsException, InvalidTokenException
from app.services.user_service import UserService


class AuthService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.user_service = UserService(db_session)

    def user_login(self, login: LoginRequest):
        user = self.user_service.get_user_by_email(login.email)
        if not user:
            raise InvalidCredentialsException()
        if not self.verify_password(login.password, user.password):
            raise InvalidCredentialsException()

        now = datetime.now()
        payload = Payload(
            id=str(user.id),
            sub=user.email,
            iat=int(now.timestamp()),
            exp=int((now + timedelta(hours=24)).timestamp())
        ).model_dump()

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return LoginResponse(
            id=str(user.id),
            firstName=user.first_name,
            lastName=user.last_name,
            email=user.email,
            role=user.role,
            token=access_token
        )

    def verify_token(self, access_token):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except ExpiredSignatureError:
            raise InvalidTokenException()
        except JWTError:
            raise InvalidTokenException()

        user = self.user_service.get_user_by_email(data["sub"])

        if not user:
            raise InvalidTokenException()

        return user
    
    def verify_password(self, plain_password: str, hashed_password: str):
        return crypt_context.verify(plain_password, hashed_password)
