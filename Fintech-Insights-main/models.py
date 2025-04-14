import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

# Step 1: Load environment variables
print("Step 1: Loading environment variables...")

load_dotenv()

# Step 2: Setup database connection
def get_db_connection():
    try:
        print("Step 2: Establishing database connection...")
        conn = psycopg2.connect(
        host=os.getenv("host"),
        port=os.getenv("port"),
        database=os.getenv("database"),
        user=os.getenv("user"),
        password=os.getenv("password")
        )
        print("Database connection established.")
        return conn
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        raise

# Create cursor
try:
    conn = get_db_connection()
    cursor = conn.cursor()
except Exception as e:
    print(f"Exiting due to connection error: {e}")
    exit(1)

# Step 3: Store market data
def store_data(data):
    print("Step 3: Storing market data...")
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_metrics (
                id SERIAL PRIMARY KEY,
                coin TEXT,
                date DATE,
                price FLOAT,
                market_cap FLOAT,
                volume FLOAT,
                price_change_24h FLOAT
            )
        """)
        cursor.execute("""
            INSERT INTO daily_metrics (coin, date, price, market_cap, volume, price_change_24h)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data["coin"], data["date"], data["price"], data["market_cap"], data["volume"], data["price_change_24h"]))
        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()

# Step 4: Get latest record
def get_latest_data():
    print("Step 4: Fetching latest market data from DB...")
    try:
        cursor.execute("""
            SELECT coin, date, price, market_cap, volume, price_change_24h
            FROM daily_metrics
            ORDER BY date DESC LIMIT 1
        """)
        row = cursor.fetchone()
        if row:
            print("Latest data fetched.")
            return {
                "coin": row[0],
                "date": row[1],
                "price": row[2],
                "market_cap": row[3],
                "volume": row[4],
                "price_change_24h": row[5],
            }
        else:
            print("No data found.")
            return {}
    except Exception as e:
        print(f"Error fetching latest data: {e}")
        return {}

# Step 5: Store recommendations
def store_recommendation(summary):
    print("Step 5: Storing recommendation...")
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_recommendations (
                id SERIAL PRIMARY KEY,
                date DATE,
                recommendation TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO daily_recommendations (date, recommendation)
            VALUES (%s, %s)
        """, (datetime.utcnow().date(), summary))
        conn.commit()
        print("Recommendation stored successfully.")
        return "Insertion Successful"
    except Exception as e:
        print(f"Error storing recommendation: {e}")
        conn.rollback()
        return "Insertion Failed"
