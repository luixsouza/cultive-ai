from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
    token_type: Optional[str] = None  # "access" or "refresh"