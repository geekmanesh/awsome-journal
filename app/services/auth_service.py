from datetime import timedelta

from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories import list_repository, user_repository
from app.schemas.user import CreateUserRequest

ACCESS_TOKEN_EXPIRE = timedelta(minutes=20)


def register_user(db: Session, create_user_request: CreateUserRequest) -> User:
    user = user_repository.create(
        db,
        email=create_user_request.email,
        name=create_user_request.name,
        role=create_user_request.role,
        hashed_password=hash_password(create_user_request.password),
    )
    list_repository.create_default(db, owner_id=user.id)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = user_repository.get_by_email(db, email)
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user


def login(db: Session, email: str, password: str) -> str | None:
    user = authenticate_user(db, email, password)
    if user is None:
        return None
    return create_access_token(user.email, user.id, user.role, ACCESS_TOKEN_EXPIRE)
