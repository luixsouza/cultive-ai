from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.base_class import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    name = Column(String(255), nullable=False)
    document = Column(String(20), nullable=True)  # CPF or CNPJ
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(2), nullable=True)
    notes = Column(String(1000), nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="clients")

    properties = relationship("Property", back_populates="client", cascade="all, delete-orphan")
