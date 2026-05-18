from pydantic import BaseModel, Field


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


class Token(BaseModel):
    access_token: str
    token_type: str
