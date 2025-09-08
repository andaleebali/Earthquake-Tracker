# app.py
from dash import Dash
from callbacks import register_callbacks
from layout import dashboard_layout

# initialise app
app = Dash(__name__)
app.title = "NZ Earthquake Tracker"

# set up dashboard layout
app.layout = dashboard_layout()

# call data and functions
register_callbacks(app)

# run app
if __name__ == "__main__":
    app.run(debug=True)
