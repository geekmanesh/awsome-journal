import uuid

from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories import user_repository
from app.schemas.user import UpdateUserRequest, UserVerification


def get_user(db: Session, user_id: uuid.UUID | str) -> User | None:
    return user_repository.get_by_id(db, user_id)


def update_user(
    db: Session, user_id: uuid.UUID | str, update_request: UpdateUserRequest
) -> User | None:
    user = user_repository.get_by_id(db, user_id)
    if user is None:
        return None
    update_data = update_request.model_dump(exclude_unset=True)
    return user_repository.update(db, user, update_data)


def change_password(
    db: Session, user_id: uuid.UUID | str, verification: UserVerification
) -> bool | None:
    """Returns None if the user doesn't exist, False if the current password is
    wrong, and True once the password has been changed."""
    user = user_repository.get_by_id(db, user_id)
    if user is None:
        return None
    if not verify_password(verification.password, user.hashed_password):
        return False
    user_repository.update_password(db, user, hash_password(verification.new_password))
    return True
