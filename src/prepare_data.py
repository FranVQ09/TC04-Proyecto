import os
import json
import pandas as pd
from collections import defaultdict

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"

def load_json(filename):
    with open(os.path.join(RAW_PATH, filename), 'r') as f:
        return json.load(f)
    
def build_dataset(seasons=[2022, 2023, 2024, 2025]):
    # Movemos la declaración de data fuera del bucle para acumular todas las temporadas
    data = []

    for season in seasons:
        print(f"Processing season {season}...")
        
        # Verificamos si los archivos existen antes de cargarlos
        if not os.path.exists(os.path.join(RAW_PATH, f"results_{season}.json")):
            print(f"Archivo results_{season}.json no encontrado. Saltando temporada {season}.")
            continue
            
        if not os.path.exists(os.path.join(RAW_PATH, f"standings_{season}.json")):
            print(f"Archivo standings_{season}.json no encontrado. Saltando temporada {season}.")
            continue
            
        results_json = load_json(f"results_{season}.json")
        standings_json = load_json(f"standings_{season}.json")

        # Diccionario con estadisticas por piloto
        pilots_stats = defaultdict(lambda: {
            "carreras": 0,
            "suma_pos": 0,
            "podios": 0,
            "abandonos": 0,
            "constructor": None 
        })

        # Resultados por carrera
        races = results_json["MRData"]["RaceTable"]["Races"]
        for race in races:
            for result in race["Results"]:
                code = result["Driver"]["code"]
                pos = result["positionText"]
                status = result["status"]
                constructor = result["Constructor"]["name"]

                pilots_stats[code]["carreras"] += 1
                pilots_stats[code]["constructor"] = constructor  # Corregido: minúscula en "constructor"

                if pos not in ("R", "D", "W", "NC"): # Abandono o no clasificado
                    pilots_stats[code]["suma_pos"] += int(pos)
                    if int(pos) <= 3:
                        pilots_stats[code]["podios"] += 1
                else:
                    pilots_stats[code]["abandonos"] += 1

        # Puntos finales desde standings
        final_points = {}
        if standings_json["MRData"]["StandingsTable"]["StandingsLists"]:
            for entry in standings_json["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]:
                code = entry["Driver"]["code"]
                points = float(entry["points"])
                final_points[code] = points

        # Datos finales por piloto
        for code, stats in pilots_stats.items():
            carreras = stats["carreras"]
            if carreras == 0:
                continue
            row = {
                "piloto": code,
                "temporada": season,
                "constructor": stats["constructor"],
                "carreras_corridas": carreras,
                "promedio_pos_final": stats["suma_pos"] / max(stats["carreras"] - stats["abandonos"], 1),
                "podios": stats["podios"],
                "abandonos": stats["abandonos"],
                "puntos_totales": final_points.get(code, 0.0)
            }
            # Añadimos cada fila a la lista data
            data.append(row)
    
    # Movido fuera del bucle para procesar todas las temporadas acumuladas
    if data:
        df = pd.DataFrame(data)
        os.makedirs(PROCESSED_PATH, exist_ok=True)
        df.to_csv(os.path.join(PROCESSED_PATH, "pilots_dataset.csv"), index=False)
        print(f"Dataset procesado guardado en data/processed/pilots_dataset.csv con {len(df)} filas")
        return df
    else:
        print("No se encontraron datos para procesar")
        return None