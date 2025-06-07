import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
from dash import Dash, html, dcc
from dash.dependencies import Input, Output


def get_earthquake_data():
    url = "https://api.geonet.org.nz/quake?MMI=1"
    response = requests.get(url)
    print(f"Status code: {response.status_code}")
    print(f"Content: {response.text[:300]}")
    data = response.json()

    # Check the number of earthquakes returned
    quakes = data.get("features", [])
    print(f"{len(quakes)} earthquakes found.")

    # Parse into DataFrame
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
    print(df.head())
    return df

app = Dash(__name__)
app.title = "NZ Earthquake Tracker"

dcc.Interval(
    id="interval-component",
    interval=5*60*1000,  # 5 minutes in milliseconds
    n_intervals=0
)

app.layout = html.Div([
    html.H1("🌀 Real-Time NZ Earthquake Dashboard"),
    dcc.Graph(id="quake-map"),
    # Magnitude filter slider
    html.Label("Minimum Magnitude:"),
    dcc.Slider(
        id="magnitude-slider",
        min=0,
        max=10,
        step=0.1,
        value=1,
        marks={i: str(i) for i in range(11)},
    ),
    dcc.Graph(id="fig"),
    dcc.Graph(id="time-series"),
    html.Div(id="last-updated", style={"fontSize": "0.9em", "color": "gray", "marginTop": "10px"}),
    html.P("Data source: GeoNet API", style={"fontSize": "0.9em", "color": "gray"}),
    dcc.Interval(id="interval-component", interval=5*60*1000, n_intervals=0)
])

@app.callback(
    Output("quake-map", "figure"),
    Output('fig','figure'),
    Output("time-series", "figure"),
    Output("last-updated", "children"),
    Input("interval-component", "n_intervals"),  # Dummy trigger to run once
    Input("magnitude-slider", "value")
)


def update_map(n_intervals, min_magnitude):
    df = get_earthquake_data()

    filtered_df = df[
        df["magnitude"]>=min_magnitude
    ] 

    map=px.scatter_map(
        data_frame=filtered_df,
        lat='lat',
        lon='lon',
        size='magnitude',
        color='magnitude',
        zoom=4,
        center={"lat": -41.0, "lon": 174.0}
    )
    map.update_layout(mapbox_style="open-street-map")
    map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # Magnitude vs Depth scatter
    depth_fig = px.scatter(
        data_frame=filtered_df,
        x='depth',
        y='magnitude',
        title="Magnitude vs Depth"
    )

    # Time Series of Magnitude over Time
    time_fig = px.line(
        data_frame=filtered_df.sort_values('time'),
        x='time',
        y='magnitude',
        title="Magnitude over Time"
    )


    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    last_updated_str = f"Last updated at: {timestamp}"

    return map, depth_fig, time_fig, last_updated_str

if __name__ == "__main__":
    app.run(debug=True)