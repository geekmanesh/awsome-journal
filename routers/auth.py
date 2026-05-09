from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from database import session_local
from models.user import CreateUserRequest, Token, User
from settings import ALGORITHM, SECRET_KEY

router = APIRouter()


def get_db():
    sqlite_db = session_local()

    try:
        yield sqlite_db
    finally:
        sqlite_db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(
    username: str,
    user_id: int,
    expire_delta: timedelta,
):
    encode = {
        "sub": username,
        "id": user_id,
    }
    expires = datetime.now(timezone.utc) + expire_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(
    db: db_dependency,
    create_user_request: CreateUserRequest,
):
    create_user_model = User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Failed authentication"
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return Token(access_token=token, token_type="bearer")
