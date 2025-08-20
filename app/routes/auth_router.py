from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.DTOs.auth_dtos import LoginRequest, LoginResponse
from app.services.auth_service import AuthService
from app.utils.depends import get_db_session


auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    description="Rota pública. Permite login de qualquer usuário registrado. Não requer autenticação prévia.\n\nApós fazer login, acrescente o token retornado no campo `Authorize` do Swagger para autenticação nas rotas protegidas."
)
def user_login(
    login_request: LoginRequest,
    db_session: Session = Depends(get_db_session),
):
    auth_service = AuthService(db_session=db_session)
    user_data = auth_service.user_login(login=login_request)
    return LoginResponse(
        id=user_data.id,
        firstName=user_data.firstName,
        lastName=user_data.lastName,
        email=user_data.email,
        role=user_data.role,
        token=user_data.token
    )
