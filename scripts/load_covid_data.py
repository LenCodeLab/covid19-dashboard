import os
import pandas as pd
import psycopg2
import logging
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Setup logging
logging.basicConfig(
    filename="cron.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Database configuration
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

CSV_PATH = os.path.join("data", "latest.csv")

# Utility function for safe integer conversion
def safe_int(val):
    try:
        if pd.isna(val) or val == '':
            return None
        return int(float(val))
    except (ValueError, TypeError):
        return None

def load_data():
    try:
        df = pd.read_csv(CSV_PATH)

        # Rename and select only relevant columns
        df = df.rename(columns={'last_updated_date': 'date'})
        required_columns = ['iso_code', 'continent', 'location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']
        df = df[required_columns]

        # Drop rows with missing or invalid date
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])

        # Connect to DB
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()

        # Clean existing data
        cur.execute("DELETE FROM covid_data;")

        # Insert rows
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO covid_data (
                    iso_code, continent, location, date,
                    total_cases, new_cases, total_deaths, new_deaths
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                row['iso_code'],
                row['continent'],
                row['location'],
                row['date'].date(),  # ensure it's a Python date object
                safe_int(row['total_cases']),
                safe_int(row['new_cases']),
                safe_int(row['total_deaths']),
                safe_int(row['new_deaths'])
            ))

        conn.commit()
        cur.close()
        conn.close()
        logging.info("✅ Data loaded successfully.")
        print("✅ Data loaded successfully.")

    except Exception as e:
        logging.error(f"❌ Failed to load data: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    load_data()
