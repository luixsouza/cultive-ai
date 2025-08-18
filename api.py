from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Dict, Any, List
import ee
from fastapi.middleware.cors import CORSMiddleware
import config, ee_utils, ai_analysis, map_utils

app = FastAPI(title="GeoMapIFG API")

origins = ["http://localhost", "http://localhost:8080", "http://127.0.0.1", "http://127.0.0.1:5500", "null"]
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

class GeoJSONInput(BaseModel):
    type: str = Field(..., example="FeatureCollection")
    features: List[Dict[str, Any]] = Field(..., min_items=1)

class AnalysisResponse(BaseModel):
    aoi_area_hectares: float
    analysis_period: Dict[str, str]
    satellite_image_info: Dict[str, Any]
    ndvi_stats: Dict[str, float | None]
    degradation_summary: List[Dict[str, Any]]
    ai_description: str
    map_layers: Dict[str, str | None]

def run_analysis(geojson_data: dict):
    try:
        ee_utils.initialize_earthengine()
        aoi = ee.Geometry(geojson_data['features'][0]['geometry'])
        start_date, end_date = ee_utils.get_date_range()
        
        results = ee_utils.process_analysis_layers(aoi, start_date, end_date)
        (classified, ndvi, ndmi, savi, slope, mapbiomas, rgb, s2_img, stats, px_counts) = results

        if classified is None or not stats:
            raise RuntimeError("Não foi possível processar as imagens do GEE.")

        aoi_area_ha = ee_utils.get_aoi_area(aoi) / 10000

        cleaned_stats = {'min': stats.get('NDVI_min'), 'mean': stats.get('NDVI_mean'), 'max': stats.get('NDVI_max')}
        ai_desc = ai_analysis.generate_ai_description(cleaned_stats, px_counts, aoi_area_ha * 10000)
        
        map_layers = {
            'rgb_url': map_utils.get_ee_tile_url(rgb, {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000}, 'RGB'),
            'degradation_url': map_utils.get_ee_tile_url(classified, config.DEGRADATION_VIS_PARAMS, 'Degradation'),
            'ndvi_url': map_utils.get_ee_tile_url(ndvi, config.NDVI_VIS_PARAMS, 'NDVI'),
            'ndmi_url': map_utils.get_ee_tile_url(ndmi, config.NDMI_VIS_PARAMS, 'NDMI'),
            'savi_url': map_utils.get_ee_tile_url(savi, config.SAVI_VIS_PARAMS, 'SAVI'),
            'slope_url': map_utils.get_ee_tile_url(slope, config.SLOPE_VIS_PARAMS, 'Slope'),
            'mapbiomas_url': map_utils.get_ee_tile_url(mapbiomas, config.MAPBIOMAS_VIS_PARAMS, 'MapBiomas')
        }

        summary = []
        total_pixels = sum(px_counts.values())
        for class_id, count in px_counts.items():
            class_name = config.DEGRADATION_CLASS_NAMES.get(str(int(float(class_id))), "Desconhecida")
            percentage = (count / total_pixels) * 100
            area_ha = count * (30*30) / 10000
            summary.append({"class_name": class_name, "percentage": round(percentage, 2), "area_hectares": round(area_ha, 2)})

        img_info = {'id': s2_img.get('system:index').getInfo(), 'cloud_percentage': round(s2_img.get('CLOUDY_PIXEL_PERCENTAGE').getInfo(), 2)}

        return {
            "aoi_area_hectares": round(aoi_area_ha, 2),
            "analysis_period": {'start_date': start_date.format('YYYY-MM-dd').getInfo(), 'end_date': end_date.format('YYYY-MM-dd').getInfo()},
            "satellite_image_info": img_info,
            "ndvi_stats": {k: (round(v, 4) if v is not None else None) for k, v in cleaned_stats.items()},
            "degradation_summary": summary, "ai_description": ai_desc, "map_layers": map_layers
        }
    except Exception as e:
        print(f"ERRO GERAL na análise: {e}")
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro interno durante a análise: {e}")

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_area(geojson: GeoJSONInput = Body(...)):
    return run_analysis(geojson.dict())

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API GeoMapIFG."}