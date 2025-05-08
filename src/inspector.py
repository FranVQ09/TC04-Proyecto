import os
import json

# Inspeccionar la estructura de los datos para entender el problema
def inspect_results_file(season):
    filepath = f"data/raw/results_{season}.json"
    if not os.path.exists(filepath):
        print(f"El archivo {filepath} no existe")
        return
    
    with open(filepath, 'r') as f:
        results = json.load(f)
    
    # Estructura general
    print(f"\n=== Estructura de results_{season}.json ===")
    
    # Información MRData
    mr_data = results.get("MRData", {})
    print(f"Versión: {mr_data.get('xmlns', 'N/A')}")
    
    # Información de tablas
    race_table = mr_data.get("RaceTable", {})
    print(f"Season: {race_table.get('season', 'N/A')}")
    
    # Contar carreras
    races = race_table.get("Races", [])
    print(f"Número total de carreras: {len(races)}")
    
    # Información sobre la primera carrera
    if races:
        first_race = races[0]
        print(f"\nEjemplo - Primera carrera:")
        print(f"  Round: {first_race.get('round')}")
        print(f"  Nombre: {first_race.get('raceName')}")
        
        # Inspeccionar resultados
        results_list = first_race.get("Results", [])
        print(f"  Número de resultados en esta carrera: {len(results_list)}")
        
        if results_list:
            first_result = results_list[0]
            print(f"\n  Primer resultado:")
            print(f"    Posición: {first_result.get('position')}")
            print(f"    Piloto: {first_result.get('Driver', {}).get('code')}")
            print(f"    Constructor: {first_result.get('Constructor', {}).get('name')}")
    
    # Contar pilotos únicos
    pilotos = set()
    for race in races:
        for result in race.get("Results", []):
            driver_code = result.get("Driver", {}).get("code")
            if driver_code:
                pilotos.add(driver_code)
    
    print(f"\nNúmero total de pilotos únicos: {len(pilotos)}")
    print(f"Pilotos: {', '.join(sorted(pilotos))}")
    
    # Analizar distribución de carreras por piloto
    carreras_por_piloto = {}
    for race in races:
        race_round = race.get("round")
        for result in race.get("Results", []):
            driver_code = result.get("Driver", {}).get("code")
            if driver_code:
                if driver_code not in carreras_por_piloto:
                    carreras_por_piloto[driver_code] = set()
                carreras_por_piloto[driver_code].add(race_round)
    
    print("\nCarreras por piloto:")
    for piloto, carreras in sorted(carreras_por_piloto.items()):
        print(f"  {piloto}: {len(carreras)} carreras")

# Ejecutar para una temporada específica
inspect_results_file(2022)