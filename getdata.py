'''
Functions for ingesting, cleaning, and summarising earthquake data 
from GeoNet API.
'''

import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
import json

def get_earthquake_data():
    '''
    Fetches data from GeoNet API

    Returns:
        df (dataframe): contains earthquake records
        - publicID (str): Unique event ID
        - time (datetime): Event timestamp (UTC)
        - magnitude (float): Richter scale magnitude
        - depth (float): Depth in km
        - locality (str): Nearest named place
        - lat, lon (float): Event coordinates
    '''
    
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

def save_to_json(df):
    '''
    Saves new earthquake records to JSON file
    
    Parameters:
        df : pd.DataFrame
            Earthquake records

    '''
    df['time'] = pd.to_datetime(df['time'])
    df['time'] = df['time'].dt.strftime('%Y-%m-%dT%H:%M:%S')

    data = df.to_dict(orient='records')

    with open ('earthquakes.json', 'w') as f:
        json.dump(data, f, indent=3)

if __name__=='__main__':
    df = get_earthquake_data()
    j = save_to_json(df)
    print(j)
