import requests
import os
import json 
import time

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
    all_races = []
    offset = 0
    limit = 100 
    total = None
    
    # Continue fetching until we have all results
    while total is None or offset < total:
        url = f"{BASE_URL}/{season}/results.json?limit={limit}&offset={offset}"
        
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            results = response.json()
            mr_data = results.get("MRData", {})
            
            # Get the total number of results if we don't have it yet
            if total is None:
                total = int(mr_data.get("total", "0"))
            
            # Extract races from this page
            races = mr_data.get("RaceTable", {}).get("Races", [])
            
            # Add to our collection
            all_races.extend(races)
            
            # Update offset for next request
            offset += limit
            
            # Optional: add a small delay to prevent overwhelming the API
            time.sleep(0.5)
        else:
            raise Exception(f"Error fetching results for {season} at offset {offset}: {response.status_code}")
    
    # Create a complete result object
    complete_results = {
        "MRData": {
            "xmlns": mr_data.get("xmlns", ""),
            "series": mr_data.get("series", ""),
            "url": mr_data.get("url", ""),
            "limit": str(total),
            "offset": "0",
            "total": str(total),
            "RaceTable": {
                "season": str(season),
                "Races": all_races
            }
        }
    }
    
    print(f"Successfully fetched all {len(all_races)} races for season {season}")
    
    if save:
        save_json(complete_results, f"data/raw/results_{season}.json")
    
    return complete_results


def get_driver_standings(season: int, save=True):
    all_standings = []
    offset = 0
    limit = 100
    total = None
    
    # Continue fetching until we have all results
    while total is None or offset < total:
        url = f"{BASE_URL}/{season}/driverStandings.json?limit={limit}&offset={offset}"
        
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            mr_data = data.get("MRData", {})
            
            # Get the total number of results if we don't have it yet
            if total is None:
                total = int(mr_data.get("total", "0"))
            
            # Extract standings from this page
            standings_tables = mr_data.get("StandingsTable", {}).get("StandingsLists", [])
            
            # Add to our collection
            all_standings.extend(standings_tables)
            
            # Update offset for next request
            offset += limit
            
            # Optional: add a small delay to prevent overwhelming the API
            time.sleep(0.5)
        else:
            raise Exception(f"Error fetching standings for {season} at offset {offset}: {response.status_code}")
    
    # Create a complete result object
    complete_standings = {
        "MRData": {
            "xmlns": mr_data.get("xmlns", ""),
            "series": mr_data.get("series", ""),
            "url": mr_data.get("url", ""),
            "limit": str(total),
            "offset": "0",
            "total": str(total),
            "StandingsTable": {
                "season": str(season),
                "StandingsLists": all_standings
            }
        }
    }
    
    print(f"Successfully fetched all {len(all_standings)} standings entries for season {season}")
    
    if save:
        save_json(complete_standings, f"data/raw/standings_{season}.json")
    
    return complete_standings