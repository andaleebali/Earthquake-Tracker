# getdata.py

import requests
import pandas as pd
from datetime import datetime, timedelta, timezone

def get_earthquake_data():
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
    time_threshold = datetime.now(timezone.utc) - timedelta(hours=time_range_hours)

    filtered_df = df[
        (df["magnitude"] >= min_magnitude) &
        (df["depth"] <= max_depth) &
        (df["time"] >= time_threshold)
    ]

    return filtered_df

def summary_stats(df):
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
