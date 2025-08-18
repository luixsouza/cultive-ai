import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLOUD_PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT_ID')

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_GENERATION_CONFIG = {
    "temperature": 0.7, "top_p": 0.95, "top_k": 64, "max_output_tokens": 512,
}
GEMINI_MODEL_NAME = "gemini-1.5-flash-latest"

SENTINEL2_COLLECTION_ID = 'COPERNICUS/S2_SR_HARMONIZED'
CLOUD_FILTER_PERCENTAGE = 20

PASTURE_NDVI_THRESHOLDS = {
    'severa': 0.15, 'moderada': 0.3, 'estressada': 0.5, 'boa': 0.7, 'excelente': 1.0
}

DEGRADATION_CLASS_NAMES = {
    '0': 'Não Classificado', '1': 'Degradação Severa', '2': 'Degradação Moderada',
    '3': 'Pastagem Estressada', '4': 'Pastagem Boa', '5': 'Pastagem Excelente'
}

NDVI_VIS_PARAMS = {
    'min': -0.2, 'max': 0.8,
    'palette': ['#d73027', '#fc8d59', '#fee08b', '#d9ef8b', '#91cf60', '#1a9850']
}

DEGRADATION_COLORS = {
    '0': '#CCCCCC', '1': '#a50026', '2': '#d73027',
    '3': '#fdae61', '4': '#66bd63', '5': '#1a9641'
}

DEGRADATION_VIS_PARAMS = {
    'min': 0, 'max': 5,
    'palette': [DEGRADATION_COLORS[str(i)] for i in range(6)], 'opacity': 0.7
}

NDMI_VIS_PARAMS = {
    'min': -1, 'max': 1,
    'palette': ['#a50026','#d73027','#f46d43','#fdae61','#fee090','#ffffbf','#e0f3f8','#abd9e9','#74add1','#4575b4','#313695']
}

SAVI_VIS_PARAMS = {
    'min': 0, 'max': 1,
    'palette': ['#a50026','#d73027','#f46d43','#fdae61','#fee08b','#d9ef8b','#a6d96a','#66bd63','#1a9850']
}

SLOPE_VIS_PARAMS = {
    'min': 0, 'max': 45,
    'palette': ['#33a02c', '#b2df8a', '#fdbf6f', '#ff7f00', '#e31a1c']
}

MAPBIOMAS_VIS_PARAMS = {
    'min': 0, 'max': 62,
    'palette': [
        '#ffffff','#1f4423','#1f4423','#006400','#00ff00','#687537','#76a5af','#29eee4','#77a605',
        '#935132','#bbfcac','#45c2a5','#b8af4f','#f1c023','#db4d4f','#f40000','#fea7cb','#d33481',
        '#a40000','#8a2be2','#4b0082','#ff00ff','#c27ba0','#d5a6bd','#ffc0cb','#fff3bf','#ffd966',
        '#f6b26b','#e974ed','#e06666','#d0d0d0','#999999','#434343','#0000ff','#0000ff','#d5d5e5',
        '#dd497f','#b6184a','#af2a2a','#660000','#956857','#c29ba0','#6fa8dc','#b2ae7c','#e7875a',
        '#ff9900','#ffe500','#ffff00','#8a2be2','#000000','#8a2be2','#8a2be2','#8a2be2','#8a2be2',
        '#8a2be2','#8a2be2','#8a2be2','#8a2be2','#8a2be2','#8a2be2','#8a2be2'
    ]
}