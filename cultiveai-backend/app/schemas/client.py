from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime


class ClientBase(BaseModel):
    name: str
    document: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    notes: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    document: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    notes: Optional[str] = None


class Client(ClientBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: int
    properties_count: Optional[int] = 0

    class Config:
        from_attributes = True


class ClientWithProperties(Client):
    properties: List[Any] = []
