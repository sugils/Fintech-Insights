import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Database connection setup
import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("host"),
        port=os.getenv("port"),
        database=os.getenv("database"),
        user=os.getenv("user"),
        password=os.getenv("password")
    )
    return conn

conn = get_db_connection()
cursor = conn.cursor()


def store_data(data):
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

def get_latest_data():
    cursor.execute("""
        SELECT coin, date, price, market_cap, volume, price_change_24h
        FROM daily_metrics
        ORDER BY date DESC LIMIT 1
    """)
    row = cursor.fetchone()
    return {
        "coin": row[0],
        "date": row[1],
        "price": row[2],
        "market_cap": row[3],
        "volume": row[4],
        "price_change_24h": row[5],
    }

def store_recommendation(summary):
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
