from flask import Flask, render_template, jsonify, request
import pandas as pd
from backend.database import fetch_earthquakes
from backend.processing import filter_earthquakes, summary_stats

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/earthquakes")
def get_earthquakes():
    # Query params from frontend (with defaults)
    min_mag = float(request.args.get("min_magnitude", 0))
    max_depth = float(request.args.get("max_depth", 100))
    time_range = int(request.args.get("time_range_hours", 24))

    # Fetch from DB
    df = fetch_earthquakes()
    df_filtered = filter_earthquakes(df, min_mag, max_depth, time_range)

    # Convert DataFrame to JSON
    return jsonify(df_filtered.to_dict(orient="records"))


@app.route("/api/summary")
def api_summary():
    min_mag = float(request.args.get("min_magnitude", 1))
    max_depth = float(request.args.get("max_depth", 40))
    time_range = int(request.args.get("time_range_hours", 24))

    df = fetch_earthquakes()
    filtered = filter_earthquakes(df, min_mag, max_depth, time_range)
    row_count, largest, most_recent = summary_stats(filtered)

    return jsonify({
        "total": row_count,
        "largest": largest,
        "most_recent": most_recent
    })


if __name__ == "__main__":
    app.run(debug=True)