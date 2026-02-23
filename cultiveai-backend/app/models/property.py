from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.base_class import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    name = Column(String(255), nullable=False)
    total_area_hectares = Column(Float, nullable=True)
    geojson_boundary = Column(JSON, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(2), nullable=True)
    notes = Column(String(1000), nullable=True)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    client = relationship("Client", back_populates="properties")

    reports = relationship("AnalysisReport", back_populates="property", cascade="all, delete-orphan")
