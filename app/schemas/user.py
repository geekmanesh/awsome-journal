from pydantic import BaseModel, Field
from typing import Optional


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str


class UpdateUserRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
