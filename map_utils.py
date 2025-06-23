import folium
from . import config # Importa as configurações do módulo config

def add_ee_layer(m, ee_image, vis_params, name, overlay=True, show=True, opacity=1.0):
    """
    Adiciona uma camada de imagem do Google Earth Engine a um mapa Folium.

    Args:
        m (folium.Map): O objeto mapa Folium onde a camada será adicionada.
        ee_image (ee.Image): A imagem do Earth Engine a ser visualizada.
        vis_params (dict): Dicionário de parâmetros de visualização (cores, min/max) para a imagem.
        name (str): Nome da camada, que aparecerá no controle de camadas do Folium.
        overlay (bool, optional): Se True, a camada é uma sobreposição; se False, é uma camada base. Padrão True.
        show (bool, optional): Se True, a camada é visível ao carregar o mapa. Padrão True.
        opacity (float, optional): A opacidade da camada (0.0 a 1.0). Padrão 1.0.
    """
    try:
        map_id_dict = ee_image.getMapId(vis_params)
        folium.raster_layers.TileLayer(
            tiles=map_id_dict['tile_fetcher'].url_format,
            attr='Google Earth Engine',
            name=name,
            overlay=overlay,
            control=True,
            show=show,
            opacity=opacity
        ).add_to(m)
        print(f"DEBUG: Camada '{name}' adicionada ao mapa.")
    except Exception as e:
        print(f"ERRO: Não foi possível adicionar a camada '{name}' ao mapa: {e}")
        print("Pode ser que a imagem do Earth Engine esteja vazia ou com erro.")

def create_folium_map(aoi_geometry, ai_description, ndvi_stats, pixel_counts, aoi_area_ha, start_date_str, end_date_str):
    """
    Cria e retorna um mapa Folium interativo com as camadas de satélite,
    classificação de degradação, e um dashboard integrado com dados e descrição da IA.

    Args:
        aoi_geometry (ee.Geometry): A geometria da Área de Interesse.
        ai_description (str): A descrição textual da área gerada pela IA.
        ndvi_stats (dict): Estatísticas do NDVI para a área.
        pixel_counts (dict): Contagem de pixels por classe de degradação.
        aoi_area_ha (float): Área total da AOI em hectares.
        start_date_str (str): Data de início do período analisado (string formatada).
        end_date_str (str): Data de fim do período analisado (string formatada).

    Returns:
        folium.Map: O objeto mapa Folium configurado.
    """
    # Tenta obter o centroide e os limites da AOI para centralizar e ajustar o zoom do mapa.
    try:
        centroid = aoi_geometry.centroid().coordinates().getInfo()
        map_center = [centroid[1], centroid[0]]
        bounds = aoi_geometry.bounds().coordinates().getInfo()[0]
        folium_bounds = [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]
        m = folium.Map(location=map_center, tiles='OpenStreetMap')
        m.fit_bounds(folium_bounds)
        print("DEBUG: Mapa Folium centralizado e com zoom ajustado.")
    except Exception as e:
        print(f"ERRO: Não foi possível obter o centroide ou ajustar o zoom para a AOI: {e}")
        # Fallback para centralização e zoom padrão.
        m = folium.Map(location=config.DEFAULT_MAP_CENTER, zoom_start=config.DEFAULT_MAP_ZOOM, tiles='OpenStreetMap')

    # --- Construção do Dashboard HTML ---
    
    # CSS para o dashboard
    html_style = """
        <style>
            .map-dashboard-panel {
                position: fixed;
                top: 20px; /* Posição no topo da tela */
                right: 20px; /* Posição na direita da tela */
                width: 320px; /* Largura do painel */
                max-height: calc(100% - 40px); /* Altura máxima, com margem superior e inferior */
                overflow-y: auto; /* Rolagem vertical se o conteúdo for muito longo */
                background-color: rgba(255, 255, 255, 0.95); /* Fundo branco semi-transparente */
                border: 1px solid #ccc; /* Borda suave */
                border-radius: 8px; /* Cantos arredondados */
                box-shadow: 2px 2px 8px rgba(0,0,0,0.2); /* Sombra suave */
                padding: 15px;
                font-family: 'Segoe UI', Arial, sans-serif; /* Fonte mais limpa */
                z-index: 9999; /* Garante que fique acima do mapa */
            }
            .map-dashboard-panel h3 {
                color: #0056b3; /* Azul escuro para títulos */
                margin-top: 0;
                margin-bottom: 10px;
                font-size: 1.2em;
                border-bottom: 1px solid #eee; /* Linha separadora */
                padding-bottom: 5px;
            }
            .map-dashboard-panel h4 {
                color: #333;
                margin-top: 15px;
                margin-bottom: 8px;
                font-size: 1.05em;
            }
            .data-section p, .data-section ul {
                margin: 0 0 5px 0;
                padding: 0;
                font-size: 0.95em;
                color: #555;
            }
            .data-section ul {
                list-style-type: none; /* Remove marcadores de lista padrão */
            }
            .legend-item {
                display: flex;
                align-items: center;
                margin-bottom: 4px;
            }
            .legend-color-box {
                width: 18px;
                height: 14px;
                border-radius: 3px;
                margin-right: 8px;
                border: 1px solid #ddd;
                flex-shrink: 0; /* Previne que a caixa de cor encolha */
            }
            .ai-description-section {
                border-top: 1px dashed #e0e0e0; /* Divisor para a descrição da IA */
                padding-top: 15px;
                margin-top: 15px;
            }
        </style>
    """

    # Conteúdo do Dashboard
    dashboard_content = f"""
        <div class="map-dashboard-panel">
            <h3>Análise de Pastagem - {start_date_str} a {end_date_str}</h3>

            <div class="data-section">
                <h4>Visão Geral da Área</h4>
                <p>Área Total Mapeada: <strong>{aoi_area_ha:.2f} ha</strong></p>
            </div>

            <div class="data-section">
                <h4>Estatísticas de NDVI</h4>
                <ul>
                    <li>NDVI Mínimo: <strong>{ndvi_stats['min'] if ndvi_stats else 'N/A':.3f}</strong></li>
                    <li>NDVI Médio: <strong>{ndvi_stats['mean'] if ndvi_stats else 'N/A':.3f}</strong></li>
                    <li>NDVI Máximo: <strong>{ndvi_stats['max'] if ndvi_stats else 'N/A':.3f}</strong></li>
                </ul>
            </div>

            <div class="data-section">
                <h4>Distribuição de Saúde da Pastagem (Pixels / Área)</h4>
                <ul>
    """
    total_pixels = sum(pixel_counts.values()) if pixel_counts else 0
    # Mapeia as classes para nomes e calcula porcentagens/áreas
    for class_id_str, count in (pixel_counts.items() if pixel_counts else {}):
        class_name = config.DEGRADATION_CLASS_NAMES.get(class_id_str, f"Classe {class_id_str} (Desconhecida)")
        percentage = (count / total_pixels) * 100 if total_pixels > 0 else 0
        area_ha = (count * 10 * 10) / 10000 if count else 0 # 1 pixel = 10m x 10m = 100m² = 0.01 ha
        # O cálculo da área por classe é mais preciso aqui, usando 100m² por pixel.
        # Alternativamente: (count / total_pixels) * aoi_area_ha se a aoi_area_ha foi derivada de forma similar
        dashboard_content += f"""
                    <li>
                        <span class="legend-color-box" style="background:{config.DEGRADATION_COLORS.get(class_id_str, '#CCCCCC')};"></span>
                        {class_name}: <strong>{percentage:.1f}%</strong> ({area_ha:.2f} ha)
                    </li>
        """
    if not pixel_counts:
        dashboard_content += "<li>N/A: Dados de distribuição não disponíveis.</li>"

    dashboard_content += f"""
                </ul>
            </div>

            <div class="ai-description-section">
                <h4>Análise da IA</h4>
                <p>{ai_description}</p>
            </div>

            <div class="data-section">
                <h4>Legenda das Classes</h4>
                <ul>
                    <li class="legend-item"><span class="legend-color-box" style="background:{config.DEGRADATION_COLORS['5']};"></span> Pastagem Excelente (NDVI &ge; 0.7)</li>
                    <li class="legend-item"><span class="legend-color-box" style="background:{config.DEGRADATION_COLORS['4']};"></span> Pastagem Boa (0.5 &le; NDVI &lt; 0.7)</li>
                    <li class="legend-item"><span class="legend-color-box" style="background:{config.DEGRADATION_COLORS['3']};"></span> Pastagem Estressada (0.3 &le; NDVI &lt; 0.5)</li>
                    <li class="legend-item"><span class="legend-color-box" style="background:{config.DEGRADATION_COLORS['2']};"></span> Degradação Moderada (0.15 &le; NDVI &lt; 0.3)</li>
                    <li class="legend-item"><span class="legend-color-box" style="background:{config.DEGRADATION_COLORS['1']};"></span> Degradação Severa (NDVI &lt; 0.15)</li>
                    <li class="legend-item"><span class="legend-color-box" style="background:{config.DEGRADATION_COLORS['0']};"></span> Não Classificado / Outros</li>
                </ul>
            </div>
        </div>
    """

    m.get_root().html.add_child(folium.Element(html_style + dashboard_content))

    return m