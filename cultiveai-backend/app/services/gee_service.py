import ee
import datetime
from ..core import config

def initialize_earthengine():
    try:
        if not ee.data._credentials:
            ee.Initialize(project=config.GOOGLE_CLOUD_PROJECT_ID)
            print(f"GEE inicializado com sucesso para o projeto: {config.GOOGLE_CLOUD_PROJECT_ID}!")
    except Exception as e:
        print(f"Erro ao inicializar o GEE: {e}. Tentando autenticar...")
        ee.Authenticate()
        ee.Initialize(project=config.GOOGLE_CLOUD_PROJECT_ID)

def get_ee_tile_url(ee_image, vis_params, name):
    try:
        map_id_dict = ee.Image(ee_image).getMapId(vis_params)
        return map_id_dict['tile_fetcher'].url_format
    except Exception as e:
        print(f"Não foi possível obter a URL do tile para a camada {name}: {e}")
        return None

def run_analysis(geojson_data: dict):
    initialize_earthengine()
    aoi = ee.Geometry(geojson_data['features'][0]['geometry'])
    end_date = ee.Date(datetime.datetime.now(datetime.timezone.utc))
    start_date = end_date.advance(-6, 'month')

    s2_collection = (
        ee.ImageCollection(config.SENTINEL2_COLLECTION_ID)
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', config.CLOUD_FILTER_PERCENTAGE))
        .sort('CLOUDY_PIXEL_PERCENTAGE')
    )
    
    image_count = s2_collection.size().getInfo()
    if image_count == 0:
        raise RuntimeError("Nenhuma imagem encontrada no período para esta AOI. Tente aumentar o período ou a porcentagem de nuvens.")

    s2_image = ee.Image(s2_collection.first())
    
    ndvi = s2_image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    ndmi = s2_image.normalizedDifference(['B8', 'B11']).rename('NDMI')
    savi = s2_image.expression('((NIR - RED) / (NIR + RED + 0.5)) * 1.5', {'NIR': s2_image.select('B8'), 'RED': s2_image.select('B4')}).rename('SAVI')
    dem = ee.Image('USGS/SRTMGL1_003')
    slope = ee.Terrain.slope(dem).rename('slope')
    mapbiomas = ee.Image('projects/mapbiomas-workspace/public/collection_9/mapbiomas_collection_9_0_integration_v1').select(['classification_2022'])

    classified = ee.Image(1).where(ndvi.gte(0.3), 2).where(ndvi.gte(0.5), 3).where(ndvi.gte(0.7), 4).where(ndvi.gte(0.8), 5)
    classified = classified.rename('classification')

    aoi_area_ha = aoi.area(maxError=1).getInfo() / 10000

    stats = ndvi.reduceRegion(
        reducer=ee.Reducer.minMax().combine(ee.Reducer.mean(), sharedInputs=True),
        geometry=aoi, scale=30, maxPixels=1e9
    ).getInfo()

    px_counts_dict = classified.reduceRegion(
        reducer=ee.Reducer.frequencyHistogram(), geometry=aoi, scale=30, maxPixels=1e9
    ).get('classification').getInfo() or {}

    cleaned_stats = {'min': stats.get('NDVI_min'), 'mean': stats.get('NDVI_mean'), 'max': stats.get('NDVI_max')}

    summary = []
    total_pixels = sum(px_counts_dict.values())
    if total_pixels > 0:
        for class_id, count in px_counts_dict.items():
            class_name = config.DEGRADATION_CLASS_NAMES.get(str(int(float(class_id))), "Desconhecida")
            percentage = (count / total_pixels) * 100
            area_ha = (count * (10*10) / 10000) * aoi_area_ha / (total_pixels * (10*10)/10000)
            summary.append({"class_name": class_name, "percentage": round(percentage, 2), "area_hectares": round(area_ha, 2)})

    img_info = {
        'id': s2_image.get('system:index').getInfo(),
        'cloud_percentage': round(s2_image.get('CLOUDY_PIXEL_PERCENTAGE').getInfo(), 2)
    }

    mask = ee.Image.constant(1).clip(aoi).mask()
    map_layers_urls = {
        'rgb_url': get_ee_tile_url(s2_image.updateMask(mask), {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000}, 'RGB'),
        'degradation_url': get_ee_tile_url(classified.updateMask(mask), config.DEGRADATION_VIS_PARAMS, 'Degradation'),
        'ndvi_url': get_ee_tile_url(ndvi.updateMask(mask), config.NDVI_VIS_PARAMS, 'NDVI'),
        'ndmi_url': get_ee_tile_url(ndmi.updateMask(mask), config.NDMI_VIS_PARAMS, 'NDMI'),
        'savi_url': get_ee_tile_url(savi.updateMask(mask), config.SAVI_VIS_PARAMS, 'SAVI'),
        'slope_url': get_ee_tile_url(slope.updateMask(mask), config.SLOPE_VIS_PARAMS, 'Slope'),
        'mapbiomas_url': get_ee_tile_url(mapbiomas.updateMask(mask), config.MAPBIOMAS_VIS_PARAMS, 'MapBiomas')
    }

    return {
        "aoi_geojson": geojson_data,
        "aoi_area_hectares": round(aoi_area_ha, 2),
        "analysis_period": {'start_date': start_date.format('YYYY-MM-dd').getInfo(), 'end_date': end_date.format('YYYY-MM-dd').getInfo()},
        "satellite_image_info": img_info,
        "ndvi_stats": {k: (round(v, 4) if v is not None else None) for k, v in cleaned_stats.items()},
        "degradation_summary": summary,
        "map_layers_urls": map_layers_urls,
        "pixel_counts_for_ai": px_counts_dict
    }