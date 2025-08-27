from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.base_class import Base

class AnalysisReport(Base):
    __tablename__ = "analysis_reports"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="reports")
    
    aoi_geojson = Column(JSON, nullable=False)
    aoi_area_hectares = Column(Float)
    analysis_period = Column(JSON)
    satellite_image_info = Column(JSON)
    ndvi_stats = Column(JSON)
    degradation_summary = Column(JSON)
    ai_description = Column(Text)
    map_layers_urls = Column(JSON)
    report_html = Column(Text)