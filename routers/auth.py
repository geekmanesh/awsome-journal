from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from database import session_local
from models.user import User, CreateUserRequest

router = APIRouter()

def get_db():
    sqlite_db = session_local()

    try:
        yield sqlite_db
    finally:
        sqlite_db.close()


sqlite_db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: sqlite_db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    db.add(create_user_model)
    db.commit()

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: sqlite_db_dependency):
        user = authenticate_user(form_data.username, form_data.password, db)
        if not user:
            return "Failed authentication"
        return "successful authentication"