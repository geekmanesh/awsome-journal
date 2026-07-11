import uuid
from datetime import UTC, datetime, timedelta

from jose import jwt

from app.core.settings import ALGORITHM, SECRET_KEY

from .dependencies import bcrypt_context
from .models.user import User


def authenticate_user(email: str, password: str, db):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(
    email: str,
    user_id: uuid.UUID,
    role: str,
    expire_delta: timedelta,
):
    encode = {
        "sub": email,
        "id": str(user_id),
        "role": role,
    }
    expires = datetime.now(UTC) + expire_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
