import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta, timezone
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

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

app = Dash(__name__)
app.title = "NZ Earthquake Tracker"

app.layout = html.Div([
    html.H1("🌀 Real-Time NZ Earthquake Dashboard"),

    html.Label("Minimum Magnitude:"),
    dcc.Slider(
        id="magnitude-slider",
        min=0, max=10, step=0.1, value=1,
        marks={i: str(i) for i in range(11)}
    ),

    html.Label("Maximum Depth (km):"),
    dcc.Slider(
        id="depth-slider",
        min=0, max=100, step=1, value=40,
        marks={i: str(i) for i in range(0, 101, 10)}
    ),

    html.Label("Time Range (last X hours):"),
    dcc.Dropdown(
        id="time-range-dropdown",
        options=[
            {"label": "1 Hour", "value": 1},
            {"label": "6 Hours", "value": 6},
            {"label": "12 Hours", "value": 12},
            {"label": "24 Hours", "value": 24},
            {"label": "7 Days", "value": 168},
        ],
        value=24,
        clearable=False
    ),

    dcc.Graph(id="quake-map"),
    dcc.Graph(id="fig"),
    dcc.Graph(id="time-series"),

    html.Div(id="last-updated", style={"fontSize": "0.9em", "color": "gray", "marginTop": "10px"}),
    html.P("Data source: GeoNet API", style={"fontSize": "0.9em", "color": "gray"}),

    dcc.Interval(id="interval-component", interval=5*60*1000, n_intervals=0)
])

@app.callback(
    Output("quake-map", "figure"),
    Output("fig", "figure"),
    Output("time-series", "figure"),
    Output("last-updated", "children"),
    Input("interval-component", "n_intervals"),
    Input("magnitude-slider", "value"),
    Input("depth-slider", "value"),
    Input("time-range-dropdown", "value")
)
def update_map(n_intervals, min_magnitude, max_depth, time_range_hours):
    df = get_earthquake_data()
    time_threshold = datetime.now(timezone.utc) - timedelta(hours=time_range_hours)

    filtered_df = df[
        (df["magnitude"] >= min_magnitude) &
        (df["depth"] <= max_depth) &
        (df["time"] >= time_threshold)
    ]

    map_fig = px.scatter_mapbox(
        filtered_df,
        lat='lat', lon='lon',
        size='magnitude', color='magnitude',
        hover_name='locality',
        zoom=4,
        center={"lat": -41.0, "lon": 174.0}
    )
    map_fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})

    depth_fig = px.scatter(
        filtered_df,
        x='depth', y='magnitude',
        title="Magnitude vs Depth"
    )

    time_fig = px.line(
        filtered_df.sort_values('time'),
        x='time', y='magnitude',
        title="Magnitude over Time"
    )

    last_updated_str = f"Last updated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    return map_fig, depth_fig, time_fig, last_updated_str

if __name__ == "__main__":
    app.run(debug=True)
