from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl, validator

from functools import reduce

from uuid import UUID

from app.core.config import settings


# Shared properties
class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    avatar_url: Optional[HttpUrl] = settings.GRAVATAR_DEFAULT_URL


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str

    @validator('password')
    def must_be_long(cls, pw: str):
        assert len(pw) >= 8, 'Password must be at least 8 characters long'
        return pw

    @validator('password')
    def must_have_capital(cls, pw: str):
        assert reduce(
            lambda a, b: a or b,
            [char.isupper() for char in pw
             ]), 'Password must contain at least one uppercase character'
        return pw

    @validator('password')
    def must_have_lower(cls, pw: str):
        assert reduce(
            lambda a, b: a or b,
            [char.islower() for char in pw
             ]), 'Password must contain at least one lowercase character'
        return pw

    @validator('password')
    def must_have_numeric(cls, pw: str):
        assert reduce(
            lambda a, b: a or b,
            [char.isnumeric() for char in pw
             ]), 'Password must contain at least one numeric character'
        return pw


# Properties to receive via API on login
class UserLogin(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
