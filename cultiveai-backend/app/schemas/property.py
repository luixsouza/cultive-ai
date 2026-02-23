from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class PropertyBase(BaseModel):
    name: str
    total_area_hectares: Optional[float] = None
    geojson_boundary: Optional[Any] = None
    city: Optional[str] = None
    state: Optional[str] = None
    notes: Optional[str] = None


class PropertyCreate(PropertyBase):
    client_id: int


class PropertyUpdate(BaseModel):
    name: Optional[str] = None
    total_area_hectares: Optional[float] = None
    geojson_boundary: Optional[Any] = None
    city: Optional[str] = None
    state: Optional[str] = None
    notes: Optional[str] = None


class Property(PropertyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    client_id: int
    reports_count: Optional[int] = 0

    class Config:
        from_attributes = True


class PropertyWithClient(Property):
    client_name: Optional[str] = None
