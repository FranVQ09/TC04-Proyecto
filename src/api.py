import requests
import os
import json 

BASE_URL = "https://api.jolpi.ca/ergast/f1"

HEADERS = {
    "Accept": "application/json"
}

def save_json(data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def get_drivers_by_season(season: int, save=True):
    url = f"{BASE_URL}/{season}/drivers.json"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        drivers = response.json()
        if save:
            save_json(drivers, f"data/raw/drivers_{season}.json")
        return drivers
    else:
        raise Exception(f"Error fetching drivers for {season}: {response.status_code} - {response.text}")

def get_race_results_by_season(season: int, save=True):
    url = f"{BASE_URL}/{season}/results.json?limit=1000"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        results = response.json()
        if save:
            save_json(results, f"data/raw/results_{season}.json")
        return results
    else:
        raise Exception(f"Error fetching results for {season}: {response.status_code}")
    
def get_driver_standings(season: int, save=True):
    url = f"{BASE_URL}/{season}/driverStandings.json"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        standigs = response.json()
        if save:
            save_json(standigs, f"data/raw/standings_{season}.json")
        return standigs
    else:  
        raise Exception(f"Error fetching standings for {season}: {response.status_code} - {response.text}")

