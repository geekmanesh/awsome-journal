from fastapi import APIRouter, HTTPException, Path
from passlib.context import CryptContext
from starlette import status

from app.dependencies import db_dependency, user_dependency
from app.models.todo import TodoRequest, Todos
from app.models.user import User
from app.services import bcrypt_context

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Failed",
        )
    user_model = db.query(User).filter(User.id == user.get("id")).first()

    return user_model
