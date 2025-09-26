# callbacks.py
from dash.dependencies import Input, Output
from datetime import datetime
from dash import html
from backend.processing import filter_earthquakes, summary_stats
from visuals import earthquake_map, magnitude_vs_depth, magnitude_over_time
import pandas as pd
from backend.database import fetch_earthquakes

def register_callbacks(app):

    @app.callback(
        Output("quake-map", "figure"),
        Output("fig", "figure"),
        Output("time-series", "figure"),
        Output("quake-count", "children"),
        Output("large-mag", "children"),
        Output("most-recent", "children"),
        Output("last-updated", "children"),
        Input("interval-component", "n_intervals"),
        Input("magnitude-slider", "value"),
        Input("depth-slider", "value"),
        Input("time-range-dropdown", "value")
    )
    def update_dashboard(n_intervals, min_magnitude, max_depth, time_range_hours):
        
        records = fetch_earthquakes()
    
        df = pd.DataFrame(records)

        filtered_df = filter_earthquakes(df, min_magnitude, max_depth, time_range_hours)

        quake_count, larg_mag, most_recent = summary_stats(filtered_df)

        last_updated_str = f"Last updated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        return (
            earthquake_map(filtered_df), 
            magnitude_vs_depth(filtered_df), 
            magnitude_over_time(filtered_df), 
            quake_count,
            larg_mag,
            most_recent, 
            last_updated_str
        )