from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

class GeoJSONInput(BaseModel):
    type: str = Field(..., example="FeatureCollection")
    features: List[Dict[str, Any]] = Field(..., min_items=1)

class AnalysisResultBase(BaseModel):
    aoi_area_hectares: float
    analysis_period: Dict[str, str]
    satellite_image_info: Dict[str, Any]
    ndvi_stats: Dict[str, Optional[float]]
    degradation_summary: List[Dict[str, Any]]
    ai_description: str
    map_layers_urls: Dict[str, Optional[str]]

class AnalysisReportCreate(AnalysisResultBase):
    aoi_geojson: Dict[str, Any]
    report_html: str

class AnalysisReport(AnalysisResultBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True

class AnalysisResponse(AnalysisReport):
    pass