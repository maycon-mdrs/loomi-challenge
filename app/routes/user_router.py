from fastapi import APIRouter, Depends, status
from requests import Session

from app.DTOs.user_dtos import UserRegister, UserResponse
from app.models.user_model import UserModel
from app.services.user_service import UserService
from app.utils.depends import admin_required, get_current_user, get_db_session

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserRegister, db_session: Session = Depends(get_db_session)):
    user_service = UserService(db_session=db_session)
    user_model = user_service.register_user(user=user)
    return UserResponse(
        id=user_model.id,
        first_name=user_model.first_name,
        last_name=user_model.last_name,
        email=user_model.email,
        role=user_model.role,
    )


@user_router.get("/", response_model=list[UserResponse])
def get_all_users(
    db_session: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_current_user),
):
    user_service = UserService(db_session=db_session)
    users = user_service.get_all_users()
    return [
        UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            role=user.role,
        )
        for user in users
    ]


@user_router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    db_session: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_current_user),
):
    user_service = UserService(db_session=db_session)
    user = user_service.get_user_by_id(user_id=user_id)
    return UserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        role=user.role,
    )


@user_router.get("/email/{email}", response_model=UserResponse)
def get_user_by_email(
    email: str,
    db_session: Session = Depends(get_db_session),
    current_user: UserModel = Depends(get_current_user),
):
    user_service = UserService(db_session=db_session)
    user = user_service.get_user_by_email(email=email)
    return UserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        role=user.role,
    )


@user_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
    user_id: int,
    db_session: Session = Depends(get_db_session),
    current_user: UserModel = Depends(admin_required),
):
    user_service = UserService(db_session=db_session)
    return user_service.delete_user(user_id=user_id)
