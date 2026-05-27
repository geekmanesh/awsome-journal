from fastapi import APIRouter, HTTPException
from starlette import status

from app.dependencies import db_dependency, user_dependency
from app.models.user import User
from app.schemas.user import UpdateUserRequest, UserVerification
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


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, db: db_dependency, user_verification: UserVerification
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )

    user_model = db.query(User).filter(User.id == user.get("id")).first()

    if not bcrypt_context.verify(
        user_verification.password, user_model.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Verification falied",
        )
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)

    db.add(user_model)
    db.commit()


@router.patch("/", status_code=status.HTTP_200_OK)
async def update_user(
    user: user_dependency, db: db_dependency, user_update_request: UpdateUserRequest
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
    user_model = db.query(User).filter(User.id == user.get("id")).first()

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
        )

    update_data = user_update_request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user_model, key, value)

    db.commit()
    db.refresh(user_model)

    return user_model
