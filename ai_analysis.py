import google.generativeai as genai
from . import config

genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name=config.GEMINI_MODEL_NAME,
    generation_config=config.GEMINI_GENERATION_CONFIG
)

def generate_ai_description(ndvi_stats, pixel_counts_dict, aoi_area_sqm):
    """
    Gera uma descrição textual da área mapeada, baseada nas estatísticas de NDVI
    e na contagem de pixels por classe de degradação, utilizando a API Gemini.

    Args:
        ndvi_stats (dict): Dicionário com NDVI mínimo, médio e máximo.
        pixel_counts_dict (dict): Dicionário com a contagem de pixels para cada classe de degradação.
        aoi_area_sqm (float): Área total da AOI em metros quadrados.

    Returns:
        str: Uma descrição gerada pela IA sobre a condição da pastagem, ou uma mensagem de erro.
    """
    if not ndvi_stats or not pixel_counts_dict:
        print("DEBUG: Dados de NDVI ou contagem de pixels ausentes para a descrição da IA.")
        return "Não foi possível gerar uma descrição detalhada devido à falta de dados de NDVI ou contagem de pixels."

    aoi_area_ha = aoi_area_sqm / 10000

    prompt_parts = [
        "Você é um especialista em monitoramento de pastagens. Analise os seguintes dados de NDVI e classificação da saúde de uma pastagem e forneça uma descrição concisa e profissional, focando nas condições de degradação e saúde da área. Inclua as estatísticas principais do NDVI e a proporção de cada classe de degradação. A área total da pastagem é aproximadamente "
        f"{aoi_area_ha:.2f} hectares.\n\n",
        f"Estatísticas NDVI: Mínimo={ndvi_stats['min']:.3f}, Médio={ndvi_stats['mean']:.3f}, Máximo={ndvi_stats['max']:.3f}\n",
        "Contagem de Pixels por Classe de Degradação:\n"
    ]

    total_pixels = sum(pixel_counts_dict.values())
    
    class_percentages = {}
    for class_id_str, count in pixel_counts_dict.items():
        if class_id_str in config.DEGRADATION_CLASS_NAMES:
            class_name = config.DEGRADATION_CLASS_NAMES[class_id_str]
            percentage = (count / total_pixels) * 100 if total_pixels > 0 else 0
            class_percentages[class_name] = percentage
            prompt_parts.append(f"- {class_name}: {count} pixels ({percentage:.2f}%)\n")
        else:
             percentage = (count / total_pixels) * 100 if total_pixels > 0 else 0
             prompt_parts.append(f"- Classe {class_id_str} (Desconhecida): {count} pixels ({percentage:.2f}%)\n")
    
    prompt_parts.append("\nCom base nesses dados, descreva a condição geral da pastagem e identifique as principais preocupações ou pontos fortes.")

    try:
        print("DEBUG: Gerando descrição da IA...")
        response = model.generate_content("".join(prompt_parts))
        return response.text
    except Exception as e:
        print(f"ERRO: Falha ao gerar descrição da IA: {e}")
        return f"Não foi possível gerar a descrição da área pela IA. Verifique sua chave de API Gemini, limites de uso, ou a conexão: {e}"