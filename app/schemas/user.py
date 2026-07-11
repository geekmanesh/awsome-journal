
from pydantic import BaseModel, Field


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str


class UpdateUserRequest(BaseModel):
    name: str | None = None
    email: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
