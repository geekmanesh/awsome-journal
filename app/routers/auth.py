from datetime import timedelta

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

from app.dependencies import bcrypt_context, db_dependency
from app.models.user import User
from app.schemas.user import CreateUserRequest, Token, UserLoginRequest, UserResponse
from app.services import authenticate_user, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    summary="Register a new user",
    description="Creates a new user account with a bcrypt-hashed password. "
    "The email address must be unique.",
)
async def create_user(
    db: db_dependency,
    create_user_request: CreateUserRequest,
):
    create_user_model = User(
        email=create_user_request.email,
        name=create_user_request.name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
    )

    db.add(create_user_model)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )
    db.refresh(create_user_model)

    return create_user_model


@router.post(
    "/token",
    response_model=Token,
    summary="Log in and obtain an access token",
    description="Exchanges an email and password (JSON body) for a bearer JWT.",
)
async def login_for_access_token(
    login_request: UserLoginRequest,
    db: db_dependency,
):
    user = authenticate_user(login_request.email, login_request.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )

    token = create_access_token(
        user.email, user.id, user.role, timedelta(minutes=20)
    )

    return Token(access_token=token, token_type="bearer")
