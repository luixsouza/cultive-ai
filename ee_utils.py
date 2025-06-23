import ee
import datetime
from . import config

def initialize_earthengine():
    """
    Inicializa a API do Google Earth Engine.
    Em ambiente local, espera que as credenciais tenham sido configuradas via
    'earthengine authenticate' no terminal.
    """
    try:
        ee.Initialize(project=config.GOOGLE_CLOUD_PROJECT_ID)
        print(f"Google Earth Engine inicializado com sucesso para o projeto: {config.GOOGLE_CLOUD_PROJECT_ID}!")
    except ee.EEException as e:
        print(f"Erro ao inicializar o Google Earth Engine: {e}")
        print("Por favor, execute 'earthengine authenticate' no seu terminal para configurar as credenciais.")
        print("Certifique-se também de que seu projeto GCP está configurado e a API do Earth Engine habilitada.")
        raise

def calculate_ndvi_and_classify(aoi, date_range_months=6):
    """
    Calcula o NDVI para a Área de Interesse (AOI), classifica a pastagem em níveis de degradação,
    e extrai estatísticas do NDVI e contagem de pixels por classe.

    Args:
        aoi (ee.Geometry): Objeto ee.Geometry representando a Área de Interesse.
        date_range_months (int): Número de meses para retroceder a partir da data atual
                                 para buscar imagens de satélite.

    Returns:
        tuple: Contém os seguintes elementos:
            - ee.Image: Imagem classificada da degradação da pastagem.
            - ee.Image: Imagem de NDVI contínuo.
            - ee.Image: Imagem RGB da área (recortada para a AOI) para visualização de fundo.
            - ee.Image: A imagem original do Sentinel-2 (não recortada) para metadados.
            - dict: Dicionário com NDVI mínimo, médio e máximo da AOI. Retorna None se não houver imagem.
            - dict: Dicionário com a contagem de pixels para cada classe de degradação.
    """
    current_date = datetime.datetime.now(datetime.timezone.utc).date()
    ee_end_date = ee.Date.fromYMD(current_date.year, current_date.month, current_date.day)
    ee_start_date = ee_end_date.advance(-date_range_months, 'month')

    start_date_str = ee_start_date.format('YYYY-MM-DD').getInfo()
    end_date_str = ee_end_date.format('YYYY-MM-DD').getInfo()

    print(f"DEBUG: Filtrando coleção Sentinel-2 para AOI.")
    print(f"DEBUG: Datas de filtro: {start_date_str} a {end_date_str}")

    collection = ee.ImageCollection(config.SENTINEL2_COLLECTION_ID) \
        .filterBounds(aoi) \
        .filterDate(ee_start_date, ee_end_date) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', config.CLOUD_FILTER_PERCENTAGE))

    collection_size = collection.size().getInfo()
    print(f"DEBUG: Número de imagens na coleção após filtros: {collection_size}")

    image = collection.sort('CLOUDY_PIXEL_PERCENTAGE').first()

    if not image:
        print(f"ERRO: Nenhuma imagem Sentinel-2 encontrada para o período {start_date_str} a {end_date_str} na sua área com menos de {config.CLOUD_FILTER_PERCENTAGE}% de nuvens.")
        print("SUGESTÃO: Tente um período de datas diferente, uma área maior, ou aumente o limite de nuvens (e.g., CLOUDY_PIXEL_PERCENTAGE < 20).")
        return None, None, None, None, None, None

    original_s2_image = image
    image_clipped = image.clip(aoi)
    print("DEBUG: Imagem Sentinel-2 clipada com sucesso.")

    red = image_clipped.select('B4')
    nir = image_clipped.select('B8')

    ndvi = nir.subtract(red).divide(nir.add(red).add(1e-6)).rename('NDVI')
    print("DEBUG: NDVI calculado com sucesso.")

    # --- Cálculo de Estatísticas do NDVI (Mínimo, Médio, Máximo) ---
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
        print(f"DEBUG: Estatísticas NDVI calculadas: {ndvi_statistics}")
    except Exception as e:
        print(f"ERRO: Não foi possível calcular estatísticas NDVI: {e}")

    # --- Classificação da Degradação da Pastagem ---
    degradation_base = ee.Image.constant(0).rename('Degradacao')
    degradation_initialized = degradation_base.reproject(crs=ndvi.projection().crs(), scale=ndvi.projection().nominalScale())

    degradation_classified = degradation_initialized.where(ndvi.lt(config.PASTURE_NDVI_THRESHOLDS['severa']), 1)
    degradation_classified = degradation_classified.where(ndvi.gte(config.PASTURE_NDVI_THRESHOLDS['severa']).And(ndvi.lt(config.PASTURE_NDVI_THRESHOLDS['moderada'])), 2)
    degradation_classified = degradation_classified.where(ndvi.gte(config.PASTURE_NDVI_THRESHOLDS['moderada']).And(ndvi.lt(config.PASTURE_NDVI_THRESHOLDS['estressada'])), 3)
    degradation_classified = degradation_classified.where(ndvi.gte(config.PASTURE_NDVI_THRESHOLDS['estressada']).And(ndvi.lt(config.PASTURE_NDVI_THRESHOLDS['boa'])), 4)
    degradation_classified = degradation_classified.where(ndvi.gte(config.PASTURE_NDVI_THRESHOLDS['boa']), 5)
    print("DEBUG: Classificação de degradação aplicada.")

    # --- Contagem de Pixels por Classe de Degradação ---
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
        print(f"DEBUG: Contagem de pixels por classe: {pixel_counts}")

    except Exception as e:
        print(f"ERRO: Não foi possível contar pixels por classe de degradação: {e}")
        pixel_counts = None

    rgb_image_clipped = image_clipped.select(['B4', 'B3', 'B2']).visualize(
        min=0, max=3000, gamma=1.4
    )
    print("DEBUG: Imagem RGB clipada para visualização criada.")

    return degradation_classified, ndvi, rgb_image_clipped, original_s2_image, ndvi_statistics, pixel_counts

def get_aoi_area(aoi):
    """Calcula a área da AOI em metros quadrados."""
    return aoi.area().getInfo()