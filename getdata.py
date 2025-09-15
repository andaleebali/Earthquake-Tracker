'''
Functions for ingesting, cleaning, and summarising earthquake data 
from GeoNet API. Provides filtering and summary stats 
to support the dashboard.
'''

import requests
import pandas as pd
from datetime import datetime, timedelta, timezone

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

def filter_earthquakes(df, min_magnitude, max_depth, time_range_hours):
    '''
    Filters earthquakes by magnitude, depth, and recency.

    Parameters:
        df : pd.DataFrame
            Earthquake records from get_earthquake_data()
        min_magnitude : float
            Minimum magnitude threshold
        max_depth : float
            Maximum depth in km
        time_range_hours : int
            Number of hours to look back from now

    Returns:
        pd.DataFrame
            Filtered earthquakes
    '''
    time_threshold = datetime.now(timezone.utc) - timedelta(hours=time_range_hours)

    filtered_df = df[
        (df["magnitude"] >= min_magnitude) &
        (df["depth"] <= max_depth) &
        (df["time"] >= time_threshold)
    ]

    return filtered_df

def summary_stats(df):
    '''
    Summarises dataset

    Parameters:
        df : pd.DataFrame
            Earthquake records
    
    Returns:
        row_count : int

        largest_magnitude : float
        
        most_recent : tuple
    
    '''
    if df.empty:
        return 0, None, None

    row_count = df.shape[0]
    largest_magnitude = df['magnitude'].max()
    most_recent_row = df.loc[df['time'].idxmax()]
    most_recent_time = most_recent_row["time"].strftime("%d-%m-%Y %H:%M:%S")
    most_recent_location = most_recent_row["locality"]

    most_recent = (most_recent_time, most_recent_location)

    return row_count, largest_magnitude, most_recent

if __name__=='__main__':
    df = get_earthquake_data()
    print(df)
    rowcount, largestmagnitude, most_recent_time = summary_stats(df)
    print(rowcount, largestmagnitude, most_recent_time)
