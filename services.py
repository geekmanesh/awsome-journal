from dependencies import bcrypt_context
from models.user import User
from settings import SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta, timezone
from jose import jwt


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
    role: str,
    expire_delta: timedelta,
):
    encode = {
        "sub": username,
        "id": user_id,
        "role": role,
    }
    expires = datetime.now(timezone.utc) + expire_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
