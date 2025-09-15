'''
Functions for ingesting, cleaning, and summarising earthquake data 
from GeoNet API.
'''

import requests
import pandas as pd
import json
import os

def get_earthquake_data():
    """
    Fetches data from GeoNet API

    Returns:
        df (dataframe): contains earthquake records
        - publicID (str): Unique event ID
        - time (datetime): Event timestamp (UTC)
        - magnitude (float): Richter scale magnitude
        - depth (float): Depth in km
        - locality (str): Nearest named place
        - lat, lon (float): Event coordinates
    """
    
    url = "https://api.geonet.org.nz/quake?MMI=1"
    response = requests.get(url)
    data = response.json()

    quakes = data.get("features", [])

    records = []
    for quake in quakes:
        props = quake["properties"]
        coords = quake["geometry"]["coordinates"]
        records.append({
            "publicID": props["publicID"],
            "time": props["time"],
            "magnitude": props["magnitude"],
            "depth": props["depth"],
            "locality": props["locality"],
            "lat": coords[1],
            "lon": coords[0]
        })

    df = pd.DataFrame(records)
    df["time"] = pd.to_datetime(df["time"])
    return df

def load_json(file):
    if os.path.exists(file):
        try:
            with open (file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("JSON file invalid. Starting new file.")
            return []
    else:
        return []



def save_to_json(df, filepath="earthquakes.json"):
    '''
    Saves new earthquake records to JSON file
    
    Parameters:
        df : pd.DataFrame
            Earthquake records

    '''
    df['time'] = pd.to_datetime(df['time'])
    df['time'] = df['time'].dt.strftime('%Y-%m-%dT%H:%M:%S')

    new_records = df.to_dict(orient='records')

    existing_records = load_json(filepath)

    updated_records = {r["publicID"]: r for r in existing_records}
    for r in new_records:
        updated_records[r["publicID"]] = r   # update or add

    # Save back to file
    with open(filepath, "w") as f:
        json.dump(updated_records, f, indent=2)

    return updated_records

if __name__=='__main__':
    df = get_earthquake_data()
    j = save_to_json(df)
    print(j)
