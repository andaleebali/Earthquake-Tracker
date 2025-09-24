from backend.getdata import get_earthquake_data
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()

def get_engine():
    dbname=os.getenv("PGDATABASE")
    user=os.getenv("PGUSER")
    password=os.getenv("PGPASSWORD")
    host=os.getenv("PGHOST")
    port=os.getenv("PGPORT")
    return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")

def load_to_postgis(df):
    """
    Insert earthquake data into PostGIS table with upsert.
    """
    engine = get_engine()
    with engine.begin() as conn:
        insert_query = text("""
            INSERT INTO "earthquakes" 
            (publicID, time, magnitude, depth, locality, geom)
            VALUES (
                :publicID,
                :time,
                :magnitude,
                :depth,
                :locality,
                ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)
            )
            ON CONFLICT (publicID) DO NOTHING;
        """)
        conn.execute(insert_query, df.to_dict(orient="records"))
    print(f"✅ Inserted/updated {len(df)} earthquakes")

if __name__ == "__main__":
    df = get_earthquake_data()
    if not df.empty:
        load_to_postgis(df)
    else:
        print("ℹ️ No earthquakes retrieved from GeoNet API")