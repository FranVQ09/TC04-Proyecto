# main.py

from src.api import get_drivers_by_season, get_race_results_by_season, get_driver_standings
from src.prepare_data import build_dataset
import os

def file_exists(filename):
    return os.path.exists(os.path.join("data/raw", filename))

def fetch_all_data(seasons=[2022, 2023, 2024, 2025]):
    for year in seasons:
        print(f"\n Procesando temporada {year}...")

        if not file_exists(f"drivers_{year}.json"):
            print(" Descargando pilotos...")
            get_drivers_by_season(year)
        else:
            print(" Pilotos ya descargados.")

        if not file_exists(f"results_{year}.json"):
            print(" Descargando resultados de carreras...")
            get_race_results_by_season(year)
        else:
            print(" Resultados ya descargados.")

        if not file_exists(f"standings_{year}.json"):
            print(" Descargando clasificaciones finales...")
            get_driver_standings(year)
        else:
            print(" Clasificaciones ya descargadas.")

if __name__ == "__main__":
    fetch_all_data()
    print("\n Generando dataset final por piloto...")
    build_dataset()
