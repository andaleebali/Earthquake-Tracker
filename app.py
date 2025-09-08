# app.py

from dash import Dash
from callbacks import register_callbacks
from layout import dashboard_layout

app = Dash(__name__)
app.title = "NZ Earthquake Tracker"

app.layout = dashboard_layout()

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
