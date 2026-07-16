from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

from app.dependencies import db_dependency
from app.schemas.user import CreateUserRequest, Token, UserLoginRequest, UserResponse
from app.services import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    summary="Register a new user",
    description="Creates a new user account with a bcrypt-hashed password, along with a default "
    "\"Tasks\" list. The email address must be unique.",
)
async def create_user(
    db: db_dependency,
    create_user_request: CreateUserRequest,
):
    try:
        return auth_service.register_user(db, create_user_request)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )


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
    token = auth_service.login(db, login_request.email, login_request.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )

    return Token(access_token=token, token_type="bearer")
