from fastapi import APIRouter, HTTPException
from starlette import status

from app.dependencies import db_dependency, user_dependency
from app.models.user import User
from app.schemas.user import UpdateUserRequest, UserResponse, UserVerification
from app.services import bcrypt_context

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    summary="Get the current user",
    description="Returns the profile of the authenticated user.",
)
async def get_user(user: user_dependency, db: db_dependency):
    user_model = db.query(User).filter(User.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )

    return user_model


@router.put(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Change the current user's password",
    description="Verifies the current password before setting the new one.",
)
async def change_password(
    user: user_dependency, db: db_dependency, user_verification: UserVerification
):
    user_model = db.query(User).filter(User.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )

    if not bcrypt_context.verify(
        user_verification.password, user_model.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect.",
        )
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)

    db.add(user_model)
    db.commit()


@router.patch(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    summary="Update the current user",
    description="Partially updates the authenticated user's profile. "
    "Only the fields provided in the request body are changed.",
)
async def update_user(
    user: user_dependency, db: db_dependency, user_update_request: UpdateUserRequest
):
    user_model = db.query(User).filter(User.id == user.get("id")).first()

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )

    update_data = user_update_request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user_model, key, value)

    db.commit()
    db.refresh(user_model)

    return user_model
