import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configurações do Google Earth Engine ---
# O ID do seu projeto Google Cloud Platform (GCP).
# Obtenha-o em console.cloud.google.com
GOOGLE_CLOUD_PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT_ID', 'geomapifg') # Substitua 'geomapifg' se não usar .env

# --- Configurações da API Gemini ---
# Sua chave de API do Google Gemini.
# Crie e obtenha sua chave em makersuite.google.com/app/apikey
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'SUA_CHAVE_API_GEMINI_AQUI') # Substitua se não usar .env

# Configurações do modelo generativo (temperatura, limites de tokens, etc.)
GEMINI_GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 512,
}
# Nome do modelo Gemini a ser utilizado.
GEMINI_MODEL_NAME = "gemini-1.5-flash-latest" # Escolha com base nos modelos disponíveis na sua conta Gemini

# --- Configurações de Dados de Satélite ---
SENTINEL2_COLLECTION_ID = 'COPERNICUS/S2_SR'
CLOUD_FILTER_PERCENTAGE = 10 # % máximo de nuvens permitido na imagem

# --- Configurações de Classificação de Pastagem (Limiares de NDVI) ---
# Dicionário mapeando os IDs de classe para os limites de NDVI.
# (NDVI < LIMITE_INFERIOR) para a classe correspondente.
# A ordem é importante para o código de classificação.
PASTURE_NDVI_THRESHOLDS = {
    'severa': 0.15,        # NDVI < 0.15
    'moderada': 0.3,       # 0.15 <= NDVI < 0.3
    'estressada': 0.5,     # 0.3 <= NDVI < 0.5
    'boa': 0.7,            # 0.5 <= NDVI < 0.7
    'excelente': 1.0       # NDVI >= 0.7 (até 1.0)
}

# Nomes legíveis das classes de degradação, mapeados pelos IDs numéricos internos (0 a 5).
DEGRADATION_CLASS_NAMES = {
    '0': 'Não Classificado / Outros',
    '1': 'Degradação Severa',
    '2': 'Degradação Moderada',
    '3': 'Pastagem Estressada',
    '4': 'Pastagem Boa',
    '5': 'Pastagem Excelente'
}

# --- Configurações de Visualização (Cores) ---
NDVI_VIS_PARAMS = {
    'min': -0.2,
    'max': 0.8,
    'palette': ['#d73027', '#fc8d59', '#fee08b', '#d9ef8b', '#91cf60', '#1a9850']
}

DEGRADATION_COLORS = {
    '0': '#CCCCCC',   # Não Classificado
    '1': '#a50026',   # Degradação Severa (Vermelho Escuro)
    '2': '#d73027',   # Degradação Moderada (Vermelho Médio)
    '3': '#fdae61',   # Pastagem Estressada (Laranja)
    '4': '#66bd63',   # Pastagem Boa (Verde Médio)
    '5': '#1a9641'    # Pastagem Excelente (Verde Escuro)
}

# Parâmetros de visualização para a camada de classificação da degradação.
DEGRADATION_VIS_PARAMS = {
    'min': 0,
    'max': 5,
    'palette': [DEGRADATION_COLORS[str(i)] for i in range(6)], # Garante a ordem correta das cores
    'opacity': 0.7
}

# --- Configurações do Mapa Folium ---
MAP_OUTPUT_FILENAME = "mapa_degradacao_pastagem.html"
DEFAULT_MAP_CENTER = [-16.389, -49.348] # Centro aproximado de Inhumas, GO.
DEFAULT_MAP_ZOOM = 13