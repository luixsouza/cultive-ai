from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Integer, default=1)

    reports = relationship("AnalysisReport", back_populates="owner", cascade="all, delete-orphan")
    clients = relationship("Client", back_populates="owner", cascade="all, delete-orphan")