import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from pathlib import Path

# Load local .env (optional if you're using environment variables)
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Local DB config
LOCAL_DB_URL = os.getenv("LOCAL_DB_URL") or "postgresql://lenix:a1147@localhost:5432/covid19_dashboard"

# Render DB config (external)
RENDER_DB_URL = os.getenv("RENDER_DB_URL") or "postgresql://lenix:iXuRN58J9rmVMLDtxm32uBIQa8nolJe5@dpg-d1uf79k9c44c73cu9o3g-a.oregon-postgres.render.com/covid19_dashboard"

# Create SQLAlchemy engines
local_engine = create_engine(LOCAL_DB_URL)
render_engine = create_engine(RENDER_DB_URL)

# Define the table to migrate
TABLE_NAME = "covid_data"

def migrate_table():
    try:
        # Load data from local DB
        print(f"Fetching data from local database: {TABLE_NAME}")
        df = pd.read_sql(f"SELECT * FROM {TABLE_NAME};", local_engine)

        # Push to Render DB
        print(f"Migrating data to Render database...")
        df.to_sql(TABLE_NAME, render_engine, if_exists="replace", index=False)
        print(f"✅ Migration complete. {len(df)} rows copied to {TABLE_NAME}.")

    except Exception as e:
        print(f"❌ Error during migration: {e}")

if __name__ == "__main__":
    migrate_table()
