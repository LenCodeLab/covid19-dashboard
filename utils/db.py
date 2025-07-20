from sqlalchemy import create_engine
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Get variables securely
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Validate all necessary variables
missing_vars = [var for var in ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
                if not os.getenv(var)]

if missing_vars:
    raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

# Create database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Fetch data function
def fetch_covid_data():
    query = "SELECT * FROM covid_data;"  # adjust table name if needed
    df = pd.read_sql(query, engine)
    return df
