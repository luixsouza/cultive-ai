import ee
import datetime
import config

def initialize_earthengine():
    try:
        if not ee.data._credentials:
            ee.Initialize(project=config.GOOGLE_CLOUD_PROJECT_ID)
            print(f"GEE inicializado com sucesso para o projeto: {config.GOOGLE_CLOUD_PROJECT_ID}!")
    except Exception as e:
        print(f"Erro ao inicializar o GEE: {e}. Tentando autenticar...")
        ee.Authenticate()
        ee.Initialize(project=config.GOOGLE_CLOUD_PROJECT_ID)

def get_date_range():
    end_date = ee.Date(datetime.datetime.now(datetime.timezone.utc))
    start_date = end_date.advance(-6, 'month')
    return start_date, end_date

def process_analysis_layers(aoi, start_date, end_date):
    try:
        s2_collection = (
            ee.ImageCollection(config.SENTINEL2_COLLECTION_ID)
            .filterBounds(aoi)
            .filterDate(start_date, end_date)
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', config.CLOUD_FILTER_PERCENTAGE))
            .sort('CLOUDY_PIXEL_PERCENTAGE')
        )
        image_count = s2_collection.size().getInfo()
        if image_count == 0:
            print("AVISO: Nenhuma imagem encontrada no período para esta AOI.")
            return [None] * 10
        
        s2_image = ee.Image(s2_collection.first())

        ndvi = s2_image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        ndmi = s2_image.normalizedDifference(['B8', 'B11']).rename('NDMI')
        savi = s2_image.expression(
            '((NIR - RED) / (NIR + RED + 0.5)) * 1.5',
            {'NIR': s2_image.select('B8'), 'RED': s2_image.select('B4')}
        ).rename('SAVI')

        dem = ee.Image('USGS/SRTMGL1_003')
        slope = ee.Terrain.slope(dem).rename('slope')

        mapbiomas = ee.Image('projects/mapbiomas-workspace/public/collection_9/mapbiomas_collection_9_0_integration_v1')
        latest_band = mapbiomas.bandNames().get(mapbiomas.bandNames().size().subtract(1))
        mapbiomas_latest = mapbiomas.select([latest_band])

        thresholds = config.PASTURE_NDVI_THRESHOLDS
        classified = ee.Image(0).where(
            ndvi.lt(thresholds['moderada']), 1
        ).where(
            ndvi.lt(thresholds['estressada']).And(ndvi.gte(thresholds['moderada'])), 2
        ).where(
            ndvi.lt(thresholds['boa']).And(ndvi.gte(thresholds['estressada'])), 3
        ).where(
            ndvi.lt(thresholds['excelente']).And(ndvi.gte(thresholds['boa'])), 4
        ).where(
            ndvi.gte(thresholds['excelente']), 5
        )
        classified_degradation_raw = classified.rename('classification')
        ndvi_stats = ndvi.clip(aoi).reduceRegion(
            reducer=ee.Reducer.minMax().combine(ee.Reducer.mean(), sharedInputs=True),
            geometry=aoi, scale=30, maxPixels=1e9
        ).getInfo()

        pixel_counts_ee = classified_degradation_raw.clip(aoi).reduceRegion(
            reducer=ee.Reducer.frequencyHistogram(), geometry=aoi, scale=30, maxPixels=1e9
        ).get('classification')
        pixel_counts = pixel_counts_ee.getInfo() if pixel_counts_ee.getInfo() else {}
        mask = ee.Image.constant(1).clip(aoi).mask()
        
        return (
            classified_degradation_raw.updateMask(mask),
            ndvi.updateMask(mask),
            ndmi.updateMask(mask),
            savi.updateMask(mask),
            slope.updateMask(mask),
            mapbiomas_latest.updateMask(mask),
            s2_image.updateMask(mask),
            s2_image,
            ndvi_stats,
            pixel_counts
        )
    except Exception as e:
        print(f"ERRO durante o processamento do Earth Engine: {e}")
        return [None] * 10

def get_aoi_area(aoi):
    try:
        return aoi.area(maxError=1).getInfo()
    except Exception as e:
        print(f"Não foi possível calcular a área da AOI: {e}")
        return 0

    original_s2_image = image
    image_clipped = image.clip(aoi)
    red = image_clipped.select('B4')
    nir = image_clipped.select('B8')

    ndvi = nir.subtract(red).divide(nir.add(red).add(1e-6)).rename('NDVI')

    ndvi_statistics = None
    try:
        ndvi_stats_ee = ndvi.reduceRegion(
            reducer=ee.Reducer.min().combine(ee.Reducer.mean(), '', True).combine(ee.Reducer.max(), '', True),
            geometry=aoi,
            scale=10,
            maxPixels=1e9
        ).getInfo()
        ndvi_statistics = {
            'min': ndvi_stats_ee.get('NDVI_min'),
            'mean': ndvi_stats_ee.get('NDVI_mean'),
            'max': ndvi_stats_ee.get('NDVI_max')
        }
    except Exception as e:
        print(f"ERRO: Não foi possível calcular estatísticas NDVI: {e}")

    degradation_base = ee.Image.constant(0).rename('Degradacao')
    degradation_initialized = degradation_base.reproject(crs=ndvi.projection().crs(), scale=ndvi.projection().nominalScale())

    degradation_classified = degradation_initialized.where(ndvi.lt(config.PASTURE_NDVI_THRESHOLDS['severa']), 1)
    degradation_classified = degradation_classified.where(ndvi.gte(config.PASTURE_NDVI_THRESHOLDS['severa']).And(ndvi.lt(config.PASTURE_NDVI_THRESHOLDS['moderada'])), 2)
    degradation_classified = degradation_classified.where(ndvi.gte(config.PASTURE_NDVI_THRESHOLDS['moderada']).And(ndvi.lt(config.PASTURE_NDVI_THRESHOLDS['estressada'])), 3)
    degradation_classified = degradation_classified.where(ndvi.gte(config.PASTURE_NDVI_THRESHOLDS['estressada']).And(ndvi.lt(config.PASTURE_NDVI_THRESHOLDS['boa'])), 4)
    degradation_classified = degradation_classified.where(ndvi.gte(config.PASTURE_NDVI_THRESHOLDS['boa']), 5)

    pixel_counts = None
    try:
        image_for_grouping = degradation_classified.addBands(ee.Image.constant(1).rename('count_pixel'))

        grouped_counts_ee = image_for_grouping.reduceRegion(
            reducer=ee.Reducer.count().group(groupField=0, groupName='class'),
            geometry=aoi,
            scale=10,
            maxPixels=1e9
        ).getInfo()

        pixel_counts = {str(item['class']): item['count'] for item in grouped_counts_ee['groups']}

    except Exception as e:
        print(f"ERRO: Não foi possível contar pixels por classe de degradação: {e}")
        pixel_counts = None

    rgb_image_clipped = image_clipped.select(['B4', 'B3', 'B2']).visualize(
        min=0, max=3000, gamma=1.4
    )

    return degradation_classified, ndvi, rgb_image_clipped, original_s2_image, ndvi_statistics, pixel_counts

def get_aoi_area(aoi):
    return aoi.area().getInfo()