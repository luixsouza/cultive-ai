from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    full_name: Optional[str] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class User(UserBase):
    id: int
    full_name: Optional[str] = None
    is_active: int = 1
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True