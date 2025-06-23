import datetime
import ee
import folium

from . import config
from . import data_utils
from . import ee_utils
from . import ai_analysis
from . import map_utils

def main():
    try:
        ee_utils.initialize_earthengine()
    except Exception:
        return

    aoi = data_utils.get_geojson_input()
    if aoi is None:
        print("Não foi possível processar o GeoJSON. Encerrando.")
        return

    current_date = datetime.datetime.now(datetime.timezone.utc).date()
    ee_end_date = ee.Date.fromYMD(current_date.year, current_date.month, current_date.day)
    ee_start_date = ee_end_date.advance(-6, 'month')

    start_date_str = ee_start_date.format('YYYY-MM-DD').getInfo()
    end_date_str = ee_end_date.format('YYYY-MM-DD').getInfo()

    print(f"\nBuscando imagens Sentinel-2 entre {start_date_str} e {end_date_str}...")

    classified_degradation, ndvi_image, rgb_image_clipped, original_s2_image, ndvi_statistics, pixel_counts = \
        ee_utils.calculate_ndvi_and_classify(aoi)

    if classified_degradation is None:
        print("Não foi possível gerar os mapas. Verifique as mensagens de erro acima.")
        return

    aoi_area_sqm = ee_utils.get_aoi_area(aoi)
    aoi_area_ha = aoi_area_sqm / 10000

    if ndvi_statistics:
        print("\n--- Estatísticas do NDVI na Área de Interesse ---")
        print(f"Período Analisado: {start_date_str} a {end_date_str}")
        print(f"Área Total da AOI: {aoi_area_ha:.2f} hectares")
        print(f"NDVI Mínimo: {ndvi_statistics['min']:.3f}")
        print(f"NDVI Médio: {ndvi_statistics['mean']:.3f}")
        print(f"NDVI Máximo: {ndvi_statistics['max']:.3f}")
        print("\nNotas sobre as estatísticas:")
        print("- NDVI Min/Max: Indicam a faixa de saúde da vegetação na área, de -1 (água) a 1 (vegetação densa).")
        print("- NDVI Médio: Um valor geral da saúde da pastagem na área. Valores mais altos indicam maior biomassa vegetal.")
        print("- Para créditos de carbono, o NDVI médio ao longo do tempo (e sua variação) é mais relevante.")
        print("- Comparar o NDVI atual com períodos históricos ou áreas de referência pode dar insights sobre a degradação/recuperação.")
    else:
        print("\n--- Estatísticas do NDVI: Não disponíveis. ---")
    
    ai_description = ai_analysis.generate_ai_description(ndvi_statistics, pixel_counts, aoi_area_sqm)
    print("\n--- Descrição da Área pela IA ---")
    print(ai_description)

    # NOVO: Passar o aoi_area_ha e o período para create_folium_map
    m = map_utils.create_folium_map(
        aoi,
        ai_description,
        ndvi_statistics,
        pixel_counts,
        aoi_area_ha,
        start_date_str,
        end_date_str
    )

    map_utils.add_ee_layer(m, rgb_image_clipped, {}, 'Imagem Satélite da AOI (RGB)', overlay=False, show=True, opacity=1.0)
    map_utils.add_ee_layer(m, classified_degradation, config.DEGRADATION_VIS_PARAMS, 'Classificação da Degradação', overlay=True, show=True, opacity=config.DEGRADATION_VIS_PARAMS['opacity'])
    map_utils.add_ee_layer(m, ndvi_image, config.NDVI_VIS_PARAMS, 'NDVI Contínuo', overlay=True, show=False, opacity=0.8)

    folium.GeoJson(
        aoi.getInfo(),
        name='Borda da Área de Interesse',
        style_function=lambda x: {
            'fillColor': '#00000000',
            'color': 'blue',
            'weight': 3,
            'fillOpacity': 0
        }
    ).add_to(m)

    folium.LayerControl().add_to(m)

    m.save(config.MAP_OUTPUT_FILENAME)
    print(f"\nMapa interativo salvo em: {config.MAP_OUTPUT_FILENAME}")
    print(f"Para visualizar, abra '{config.MAP_OUTPUT_FILENAME}' no seu navegador.")

    if original_s2_image:
        try:
            image_id = original_s2_image.get('system:index').getInfo()
            cloud_perc = original_s2_image.get('CLOUDY_PIXEL_PERCENTAGE').getInfo()
            sensing_time = ee.Date(original_s2_image.get('system:time_start')).format('YYYY-MM-DD HH:mm:ss').getInfo()
            print(f"\n--- Informações da Imagem de Satélite Utilizada ---")
            print(f"ID da Imagem: {image_id}")
            print(f"Data/Hora de Aquisição: {sensing_time}")
            print(f"Porcentagem de Nuvens na Área: {cloud_perc:.2f}%")
            print(f"A imagem foi filtrada para ter menos de 10% de nuvens na área.")
        except Exception as e:
            print(f"\nNão foi possível obter todas as informações da imagem: {e}")

if __name__ == "__main__":
    main()