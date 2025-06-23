# data_utils.py
import json
import ee

def get_geojson_input():
    """
    Solicita ao usuário que insira os dados GeoJSON e os converte para um objeto ee.Geometry.
    Suporta FeatureCollection contendo Features com geometria do tipo Polygon ou MultiPolygon,
    ou uma Feature diretamente.

    Returns:
        ee.Geometry or None: O objeto ee.Geometry representando a AOI, ou None em caso de erro.
    """
    print("\n--- Por favor, insira os dados GeoJSON da sua área de interesse ---")
    print("Certifique-se de que a geometria é do tipo 'Polygon' ou 'MultiPolygon' e que o polígono está fechado.")
    print("Exemplo de GeoJSON para um polígono (substitua pelas suas coordenadas):")
    print("""
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          [
            [
              -49.36388540007576,
              -16.399974910733377
            ],
            [
              -49.3635488909766,
              -16.376811347402437
            ],
            [
              -49.33427259931531,
              -16.377779913918886
            ],
            [
              -49.33267418109256,
              -16.4018311049426
            ],
            [
              -49.364053654625394,
              -16.40021702402541
            ],
            [
              -49.36388540007576,
              -16.399974910733377]
          ]
        ],
        "type": "Polygon"
      }
    }
  ]
}
    """)
    geojson_str = input("Cole seu GeoJSON aqui (e pressione Enter): \n")
    try:
        geojson_data = json.loads(geojson_str)

        if geojson_data.get('type') == 'FeatureCollection' and 'features' in geojson_data:
            if not geojson_data['features']:
                print("Erro: O 'FeatureCollection' está vazio. Não há geometrias para processar.")
                return None
            feature = geojson_data['features'][0]
        elif geojson_data.get('type') == 'Feature' and 'geometry' in geojson_data:
            feature = geojson_data
        else:
            print("Erro: GeoJSON deve ser um 'FeatureCollection' com 'features' ou uma 'Feature' com 'geometry'.")
            return None

        if 'geometry' in feature and 'type' in feature['geometry'] and 'coordinates' in feature['geometry']:
            geom_type = feature['geometry']['type']
            coords = feature['geometry']['coordinates']

            if geom_type == 'Polygon':
                return ee.Geometry.Polygon(coords)
            elif geom_type == 'MultiPolygon':
                return ee.Geometry.MultiPolygon(coords)
            else:
                print(f"Tipo de geometria GeoJSON '{geom_type}' não suportado. Use 'Polygon' ou 'MultiPolygon'.")
                return None
        else:
            print("Erro: A feature no GeoJSON deve conter 'geometry', 'type' e 'coordinates'.")
            return None

    except json.JSONDecodeError:
        print("Erro: GeoJSON inválido. Certifique-se de que é um JSON válido.")
        return None
    except KeyError as e:
        print(f"Erro: Chave ausente no GeoJSON: {e}. Verifique a estrutura.")
        return None
    except IndexError:
        print("Erro: O 'FeatureCollection' está vazio ou não contém features válidas.")
        return None