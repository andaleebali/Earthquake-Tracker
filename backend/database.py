# database.py
import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
 
load_dotenv()

def get_engine():
    dbname=os.getenv("PGDATABASE")
    user=os.getenv("PGUSER")
    password=os.getenv("PGPASSWORD")
    host=os.getenv("PGHOST")
    port=os.getenv("PGPORT")
    return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")

def ensure_database_exists():
    """
    Connects to the default 'postgres' database and creates
    'earthquakes' if it does not already exist.
    """
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = 'earthquakes'")
        ).fetchone()
        if not result:
            conn.execute(text("CREATE DATABASE earthquakes"))
            print("✅ Database 'earthquakes' created")
        else:
            print("ℹ️ Database 'earthquakes' already exists")

def initiate_database():
    """
    Connects to 'earthquakes' and applies schema.sql (with PostGIS enabled).
    """
    engine = get_engine()
    with engine.begin() as conn:  # begin transaction
        with open("sql/schema.sql", "r") as f:
            conn.execute(text(f.read()))
    print("✅ Database initialised with schema")


def update_table(df):
    """
    Insert or update earthquake records using upsert.
    """
    engine = get_engine()
    insert_sql = text("""
        INSERT INTO "earthquakes" 
            (publicID, time, magnitude, depth, locality, geom)
        VALUES (:publicID, :time, :magnitude, :depth, :locality,
                ST_SetSRID(ST_MakePoint(:lon, :lat), 4326))
        ON CONFLICT (publicID) DO UPDATE
        SET time = EXCLUDED.time,
            magnitude = EXCLUDED.magnitude,
            depth = EXCLUDED.depth,
            locality = EXCLUDED.locality,
            geom = EXCLUDED.geom;
    """)
    with engine.begin() as conn:
        conn.execute(insert_sql, df.rename(columns={"publicID":"publicID"}).to_dict(orient="records"))
    print(f"✅ Table updated with {len(df)} rows")

def fetch_earthquakes():
    engine = get_engine()

    query = """
        SELECT
            publicid,
            time,
            magnitude,
            depth,
            locality,
            ST_X(geom) AS lon,
            ST_Y(geom) AS lat
        FROM "earthquakes"
        ORDER BY time DESC;
    """
    df = pd.read_sql(query, engine)
    return df


if __name__ == "__main__":
    from backend.getdata import get_earthquake_data
    ensure_database_exists()
    initiate_database()
    df = get_earthquake_data()
    update_table(df)
    print(fetch_earthquakes())
