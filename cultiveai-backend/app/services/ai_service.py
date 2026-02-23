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
        error_msg = str(e).lower()
        print(f"ERRO: Falha ao gerar descrição da IA: {e}")

        # Tratamento especifico para erro de quota
        if "429" in str(e) or "quota" in error_msg or "rate limit" in error_msg:
            return generate_fallback_description(ndvi_stats, pixel_counts_dict, aoi_area_sqm)

        # Outros erros
        return generate_fallback_description(ndvi_stats, pixel_counts_dict, aoi_area_sqm)


def generate_fallback_description(ndvi_stats: dict, pixel_counts_dict: dict, aoi_area_sqm: float) -> str:
    """Gera uma descricao tecnica sem usar IA quando a API esta indisponivel."""
    aoi_area_ha = aoi_area_sqm / 10000

    total_pixels = sum(pixel_counts_dict.values())
    class_percentages = {}

    if total_pixels > 0:
        for class_id_str, count in pixel_counts_dict.items():
            class_name = config.DEGRADATION_CLASS_NAMES.get(str(int(float(class_id_str))), f"Classe {class_id_str}")
            percentage = (count / total_pixels) * 100
            class_percentages[class_name] = percentage

    # Determinar condicao geral
    degradacao_severa = class_percentages.get("Degradação Severa", 0)
    degradacao_moderada = class_percentages.get("Degradação Moderada", 0)
    pastagem_estressada = class_percentages.get("Pastagem Estressada", 0)
    pastagem_boa = class_percentages.get("Pastagem Boa", 0)
    pastagem_excelente = class_percentages.get("Pastagem Excelente", 0)

    total_degradacao = degradacao_severa + degradacao_moderada
    total_saudavel = pastagem_boa + pastagem_excelente

    if total_degradacao > 50:
        condicao = "crítica"
        recomendacao_principal = "**Ação urgente recomendada:** A maior parte da área apresenta sinais de degradação significativa."
    elif total_degradacao > 30:
        condicao = "preocupante"
        recomendacao_principal = "**Atenção necessária:** Uma parcela considerável da pastagem mostra sinais de degradação."
    elif pastagem_estressada > 40:
        condicao = "moderada com estresse"
        recomendacao_principal = "**Monitoramento recomendado:** A pastagem apresenta sinais de estresse que podem evoluir para degradação."
    elif total_saudavel > 60:
        condicao = "boa"
        recomendacao_principal = "**Pastagem saudável:** A maior parte da área está em boas condições."
    else:
        condicao = "variável"
        recomendacao_principal = "**Avaliação mista:** A área apresenta condições variadas que requerem análise localizada."

    description = f"""## Relatório Técnico de Análise de Pastagem

### Área Analisada
- **Tamanho total:** {aoi_area_ha:.2f} hectares
- **Condição geral:** {condicao.upper()}

### Índices de Vegetação (NDVI)
| Métrica | Valor |
|---------|-------|
| Mínimo | {ndvi_stats['min']:.3f} |
| Médio | {ndvi_stats['mean']:.3f} |
| Máximo | {ndvi_stats['max']:.3f} |

*NDVI (Índice de Vegetação por Diferença Normalizada): valores próximos a 1 indicam vegetação densa e saudável, enquanto valores baixos ou negativos indicam solo exposto ou vegetação degradada.*

### Distribuição das Classes de Saúde

"""

    # Adicionar cada classe
    for class_name, percentage in sorted(class_percentages.items(), key=lambda x: x[1], reverse=True):
        if percentage > 0.5:  # Mostra apenas classes com mais de 0.5%
            area_ha = (percentage / 100) * aoi_area_ha
            description += f"- **{class_name}:** {percentage:.1f}% (~{area_ha:.2f} ha)\n"

    description += f"""
### Diagnóstico

{recomendacao_principal}

#### Áreas Prioritárias:
"""

    if degradacao_severa > 5:
        description += f"- 🔴 **Degradação Severa ({degradacao_severa:.1f}%):** Áreas com vegetação muito escassa ou solo exposto. Requerem intervenção imediata como ressemeadura ou renovação completa da pastagem.\n"

    if degradacao_moderada > 5:
        description += f"- 🟠 **Degradação Moderada ({degradacao_moderada:.1f}%):** Áreas com cobertura vegetal reduzida. Considerar adubação de manutenção e manejo de pastejo.\n"

    if pastagem_estressada > 10:
        description += f"- 🟡 **Pastagem Estressada ({pastagem_estressada:.1f}%):** Vegetação presente mas com sinais de estresse. Avaliar disponibilidade hídrica e pressão de pastejo.\n"

    if total_saudavel > 0:
        description += f"- 🟢 **Áreas Saudáveis ({total_saudavel:.1f}%):** Manter práticas atuais de manejo.\n"

    description += """
### Recomendações Gerais

1. **Manejo de pastejo:** Ajustar a taxa de lotação conforme a capacidade de suporte das diferentes áreas
2. **Adubação:** Considerar análise de solo nas áreas degradadas para correção de fertilidade
3. **Monitoramento:** Realizar novas análises periodicamente para acompanhar a recuperação

---
*Relatório gerado automaticamente pelo CultiveAI. Para análise mais detalhada, consulte um engenheiro agrônomo.*
"""

    return description