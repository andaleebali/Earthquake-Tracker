CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS Earthquakes (
    PublicID TEXT PRIMARY KEY,
    Time TIMESTAMP,
    Magnitude FLOAT,
    Depth FLOAT,
    Locality TEXT,
    Geom GEOMETRY(POINT, 4326)
);

CREATE INDEX IF NOT EXISTS idx_earthquakes_geom
ON Earthquakes USING GIST (Geom);