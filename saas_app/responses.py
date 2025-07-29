from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class UserCreateBody(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserCreateResponse(BaseModel):
    username: str
    email: EmailStr


class ResponseCreateUser(BaseModel):
    message: Annotated[str, Field(default="User Created")]
    user: UserCreateResponse


class ResponseGetUserBody(BaseModel):
    username: str
    email: str
