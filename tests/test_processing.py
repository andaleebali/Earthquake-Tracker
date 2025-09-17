import pytest
import pandas as pd
from processing import filter_earthquakes, summary_stats
from datetime import timedelta

def test_filter_earthquakes():
    now = pd.Timestamp("now", tz="UTC")
    testdata = pd.DataFrame([
        {"magnitude": 3.0, "depth": 10, "time": now},
        {"magnitude": 5.0, "depth": 70, "time": now},
        {"magnitude": 2.5, "depth": 20, "time": now - timedelta(hours=1)},
        {"magnitude": 4.0, "depth": 120, "time": now - timedelta(hours=2)}
    ])

    filtered_data = filter_earthquakes(testdata, min_magnitude=3, max_depth=70, time_range_hours=24)
    assert len(filtered_data)==2
    assert filtered_data.iloc[1]['depth']==70

def test_summary_stats():
    now = pd.Timestamp("now", tz="UTC")
    testdata = pd.DataFrame([
        {"magnitude": 3.0, "depth": 10, "time": now, "locality": "Auckland"},
        {"magnitude": 5.0, "depth": 70, "time": now, "locality": "Gisborne"},
        {"magnitude": 2.5, "depth": 20, "time": now - timedelta(hours=1), "locality": "Christchurch"},
        {"magnitude": 4.0, "depth": 120, "time": now - timedelta(hours=2), "locality": "Wellington"}
    ])

    count, largest, most_recent = summary_stats(testdata)

    assert count == 4
    assert largest == 5
    assert most_recent[1] == "Auckland"
