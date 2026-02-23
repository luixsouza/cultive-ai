import re
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, Any
from datetime import datetime

VALID_STATES = {
    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA",
    "MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN",
    "RS","RO","RR","SC","SP","SE","TO"
}


def validate_cpf(digits: str) -> bool:
    if len(digits) != 11:
        return False
    if len(set(digits)) == 1:
        return False
    total = sum(int(digits[i]) * (10 - i) for i in range(9))
    rest = (total * 10) % 11
    if rest == 10:
        rest = 0
    if rest != int(digits[9]):
        return False
    total = sum(int(digits[i]) * (11 - i) for i in range(10))
    rest = (total * 10) % 11
    if rest == 10:
        rest = 0
    return rest == int(digits[10])


def validate_cnpj(digits: str) -> bool:
    if len(digits) != 14:
        return False
    if len(set(digits)) == 1:
        return False
    weights1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    weights2 = [6,5,4,3,2,9,8,7,6,5,4,3,2]
    total = sum(int(digits[i]) * weights1[i] for i in range(12))
    rest = total % 11
    rest = 0 if rest < 2 else 11 - rest
    if rest != int(digits[12]):
        return False
    total = sum(int(digits[i]) * weights2[i] for i in range(13))
    rest = total % 11
    rest = 0 if rest < 2 else 11 - rest
    return rest == int(digits[13])


class ClientBase(BaseModel):
    name: str
    document: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("document")
    @classmethod
    def validate_document(cls, v):
        if v is None or v.strip() == "":
            return None
        digits = re.sub(r"\D", "", v)
        if len(digits) == 11:
            if not validate_cpf(digits):
                raise ValueError("CPF inválido")
        elif len(digits) == 14:
            if not validate_cnpj(digits):
                raise ValueError("CNPJ inválido")
        else:
            raise ValueError("Documento deve ser um CPF (11 dígitos) ou CNPJ (14 dígitos)")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if v is None or v.strip() == "":
            return None
        digits = re.sub(r"\D", "", v)
        if len(digits) not in (10, 11):
            raise ValueError("Telefone deve ter 10 ou 11 dígitos. Ex: (00) 00000-0000")
        return v

    @field_validator("state")
    @classmethod
    def validate_state(cls, v):
        if v is None or v.strip() == "":
            return None
        if v.upper() not in VALID_STATES:
            raise ValueError(f"Estado inválido: {v}")
        return v.upper()


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

    @field_validator("document")
    @classmethod
    def validate_document(cls, v):
        if v is None or v.strip() == "":
            return None
        digits = re.sub(r"\D", "", v)
        if len(digits) == 11:
            if not validate_cpf(digits):
                raise ValueError("CPF inválido")
        elif len(digits) == 14:
            if not validate_cnpj(digits):
                raise ValueError("CNPJ inválido")
        else:
            raise ValueError("Documento deve ser um CPF (11 dígitos) ou CNPJ (14 dígitos)")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if v is None or v.strip() == "":
            return None
        digits = re.sub(r"\D", "", v)
        if len(digits) not in (10, 11):
            raise ValueError("Telefone deve ter 10 ou 11 dígitos. Ex: (00) 00000-0000")
        return v

    @field_validator("state")
    @classmethod
    def validate_state(cls, v):
        if v is None or v.strip() == "":
            return None
        if v.upper() not in VALID_STATES:
            raise ValueError(f"Estado inválido: {v}")
        return v.upper()


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
