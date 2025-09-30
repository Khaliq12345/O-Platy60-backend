from pydantic import BaseModel, EmailStr
import datetime


class Login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str


class Refresh(BaseModel):
    refresh_token: str


class User(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime.datetime
    updated_at: datetime.datetime


class Session(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    user: User
