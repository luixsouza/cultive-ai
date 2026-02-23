from pydantic import BaseModel, field_validator
from typing import Optional, Any
from datetime import datetime

VALID_STATES = {
    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA",
    "MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN",
    "RS","RO","RR","SC","SP","SE","TO"
}


class PropertyBase(BaseModel):
    name: str
    total_area_hectares: Optional[float] = None
    geojson_boundary: Optional[Any] = None
    city: Optional[str] = None
    state: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("state")
    @classmethod
    def validate_state(cls, v):
        if v is None or v.strip() == "":
            return None
        if v.upper() not in VALID_STATES:
            raise ValueError(f"Estado inválido: {v}")
        return v.upper()


class PropertyCreate(PropertyBase):
    client_id: int


class PropertyUpdate(BaseModel):
    name: Optional[str] = None
    total_area_hectares: Optional[float] = None
    geojson_boundary: Optional[Any] = None
    city: Optional[str] = None
    state: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("state")
    @classmethod
    def validate_state(cls, v):
        if v is None or v.strip() == "":
            return None
        if v.upper() not in VALID_STATES:
            raise ValueError(f"Estado inválido: {v}")
        return v.upper()


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
