from fastapi import APIRouter, HTTPException
from starlette import status

from app.dependencies import db_dependency, user_dependency
from app.schemas.user import UpdateUserRequest, UserResponse, UserVerification
from app.services import user_service

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
    user_model = user_service.get_user(db, user.get("id"))
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
    result = user_service.change_password(db, user.get("id"), user_verification)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )
    if result is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect.",
        )


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
    user_model = user_service.update_user(db, user.get("id"), user_update_request)
    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )

    return user_model
