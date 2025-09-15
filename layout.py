#layout.py
from dash import html, dcc

def dashboard_layout():
    layout = html.Div([
        
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

    return layout