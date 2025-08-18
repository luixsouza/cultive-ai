import ee
import config

def get_ee_tile_url(ee_image, vis_params, name):
    """
    Gera a URL do tile para uma imagem do Google Earth Engine.

    Args:
        ee_image (ee.Image): A imagem do Earth Engine.
        vis_params (dict): Parâmetros de visualização.
        name (str): Nome da camada (para depuração).

    Returns:
        str or None: A URL do tile para a camada ou None em caso de erro.
    """
    try:
        map_id_dict = ee_image.getMapId(vis_params)
        print(f"DEBUG: URL da camada '{name}' gerada com sucesso.")
        return map_id_dict['tile_fetcher'].url_format
    except Exception as e:
        print(f"ERRO: Não foi possível obter a URL da camada '{name}': {e}")
        print("A imagem do Earth Engine pode estar vazia ou ocorreu um erro de processamento.")
        return None