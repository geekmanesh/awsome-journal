import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User


def get_by_id(db: Session, user_id: uuid.UUID | str) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create(
    db: Session,
    *,
    email: str,
    name: str,
    role: str,
    hashed_password: str,
) -> User:
    user = User(
        email=email,
        name=name,
        role=role,
        hashed_password=hashed_password,
        is_active=True,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(user)
    return user


def update(db: Session, user: User, update_data: dict) -> User:
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def update_password(db: Session, user: User, hashed_password: str) -> User:
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return user
