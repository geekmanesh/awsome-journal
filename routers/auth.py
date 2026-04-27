from calendar import firstweekday

from fastapi import FastAPI, APIRouter

from models import CreateUserRequest, User

router = APIRouter()



@router.post("/auth")
async def create_user(create_user_request: CreateUserRequest):
    create_user_request = User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=create_user_request.password
    )

