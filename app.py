# app.py

from datetime import datetime
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from getdata import get_earthquake_data, filter_earthquakes, summary_stats
from visuals import earthquake_map, magnitude_vs_depth, magnitude_over_time

app = Dash(__name__)
app.title = "NZ Earthquake Tracker"

app.layout = html.Div([
    
    html.H1("Real-Time NZ Earthquake Dashboard"),
    
    html.Div(id="summary-stats", style={"marginBottom": "20px"}),

    # Filters
    html.Div([
        html.Div([
            html.Label("Minimum Magnitude:"),
            dcc.Slider(
                id="magnitude-slider",
                min=0, max=10, step=0.1, value=1,
                marks={i: str(i) for i in range(11)}
                )], style={"flex": 1, "padding": "0 10px"}),
        
        html.Div([
            html.Label("Maximum Depth (km):"),
            dcc.Slider(
                id="depth-slider",
                min=0, max=100, step=1, value=40,
                marks={i: str(i) for i in range(0, 101, 10)}
            )], style={"flex": 1, "padding": "0 10px"}),

        html.Div([
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
            ), ], style={"flex": 1, "padding": "0 10px"}),
        ], style={"display": "flex", "marginBottom": "20px"}),

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
    Output("summary-stats", "children"),
    Output("last-updated", "children"),
    Input("interval-component", "n_intervals"),
    Input("magnitude-slider", "value"),
    Input("depth-slider", "value"),
    Input("time-range-dropdown", "value")
)
def update_dashboard(n_intervals, min_magnitude, max_depth, time_range_hours):
    df = get_earthquake_data()

    filtered_df = filter_earthquakes(df, min_magnitude, max_depth, time_range_hours)

    quake_count, larg_mag, most_recent = summary_stats(filtered_df)

    stats_div = html.Div([
        html.H3(quake_count),
        html.H3(larg_mag),
        html.H3(most_recent)
    ])

    last_updated_str = f"Last updated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    return (
        earthquake_map(filtered_df), 
        magnitude_vs_depth(filtered_df), 
        magnitude_over_time(filtered_df), 
        stats_div, 
        last_updated_str
    )

if __name__ == "__main__":
    app.run(debug=True)
