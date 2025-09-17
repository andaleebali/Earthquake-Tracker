import pytest
import pandas as pd
from getdata import get_earthquake_data, load_json, save_to_json


def test_get_earthquake_data():
    df = get_earthquake_data()
    assert not df.empty
    expected_columns = ["publicID", "time", "magnitude", "depth", "locality", "lat", "lon"]
    assert all(col in df.columns for col in expected_columns)


def test_save_load_json(tmp_path):
    test_file = tmp_path / "earthquakes.json"
    df = get_earthquake_data().head(3)
    
    # Save JSON
    save_to_json(df, filepath=test_file)
    
    # Load JSON
    records = load_json(test_file)
    assert isinstance(records, list)
    assert len(records) == 3
    assert all("publicID" in r for r in records)
