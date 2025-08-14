#visuals.py

import plotly.express as px

def earthquake_map(filtered_df):
    fig = px.scatter_mapbox(
        filtered_df,
        lat='lat', lon='lon',
        size='magnitude', color='magnitude',
        hover_name='locality',
        zoom=4,
        center={"lat": -41.0, "lon": 174.0}
    )
    fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})

    return fig

def magnitude_vs_depth(filtered_df):
    depth_fig = px.scatter(
        filtered_df,
        x='depth', y='magnitude',
        title="Magnitude vs Depth"
    )
    return depth_fig

def magnitude_over_time(filtered_df):
    time_fig = px.line(
        filtered_df.sort_values('time'),
        x='time', y='magnitude',
        title="Magnitude over Time"
    )
    return time_fig