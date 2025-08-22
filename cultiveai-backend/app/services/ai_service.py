import google.generativeai as genai
from ..core import config

genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name=config.GEMINI_MODEL_NAME,
    generation_config=config.GEMINI_GENERATION_CONFIG
)

def generate_ai_description(ndvi_stats: dict, pixel_counts_dict: dict, aoi_area_sqm: float, location_context: str = "uma área rural no Brasil"):
    if not ndvi_stats or not pixel_counts_dict:
        return "Não foi possível gerar uma descrição detalhada devido à falta de dados de NDVI ou contagem de pixels."

    aoi_area_ha = aoi_area_sqm / 10000

    prompt_parts = [
        "Você é um engenheiro agrônomo especialista em sensoriamento remoto e recuperação de pastagens degradadas. ",
        f"Analise os dados de uma área de pastagem localizada em {location_context}. ",
        "Seu laudo deve ser técnico, preciso e voltado para um produtor rural. ",
        "Forneça um diagnóstico da saúde da pastagem, aponte as áreas críticas com base na classificação de degradação e sugira possíveis manejos ou intervenções. ",
        f"A área total analisada é de aproximadamente {aoi_area_ha:.2f} hectares.\n\n",
        f"**Dados Técnicos da Análise:**\n",
        f"- **Estatísticas de NDVI:** Mínimo={ndvi_stats['min']:.3f}, Médio={ndvi_stats['mean']:.3f}, Máximo={ndvi_stats['max']:.3f}\n",
        "- **Distribuição das Classes de Saúde da Pastagem:**\n"
    ]
    
    total_pixels = sum(pixel_counts_dict.values())
    if total_pixels > 0:
        for class_id_str, count in pixel_counts_dict.items():
            class_name = config.DEGRADATION_CLASS_NAMES.get(str(int(float(class_id_str))), f"Classe {class_id_str}")
            percentage = (count / total_pixels) * 100
            prompt_parts.append(f"  - {class_name}: {percentage:.2f}%\n")
    
    prompt_parts.append(
        "\n**Diagnóstico e Recomendações:**\n"
        "Com base nos dados acima, elabore o diagnóstico da condição geral da pastagem e suas recomendações. "
        "Se houver áreas com degradação severa ou moderada, destaque-as como prioritárias. Formate sua resposta usando Markdown para melhor legibilidade."
    )

    try:
        response = model.generate_content("".join(prompt_parts))
        return response.text
    except Exception as e:
        print(f"ERRO: Falha ao gerar descrição da IA: {e}")
        return f"Não foi possível gerar a descrição da área pela IA. Erro: {e}"