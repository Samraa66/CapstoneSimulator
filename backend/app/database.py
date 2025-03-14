import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 

# ✅ Database connection

URL_DATABASE = 'postgresql://postgres:password@localhost:5432/CapstoneSimulatorDB'
DB_NAME = "CapstoneSimulatorDB"
DB_USER = "postgres"
DB_PASS = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()
def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )

def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    # ✅ Create tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            id SERIAL PRIMARY KEY,
            dep_city TEXT,
            des_city TEXT,
            distance FLOAT,
            passengers INT,
            origin_lat FLOAT,
            origin_lon FLOAT,
            dest_lat FLOAT,
            dest_lon FLOAT
        );
        
        CREATE TABLE IF NOT EXISTS trains (
            id SERIAL PRIMARY KEY,
            stop_name TEXT,
            next_stop_name TEXT,
            trip_count INT,
            total_passengers INT,
            capacity INT,
            origin_lat FLOAT,
            origin_lon FLOAT,
            dest_lat FLOAT,
            dest_lon FLOAT
        );

        CREATE TABLE IF NOT EXISTS train_trips (
            id SERIAL PRIMARY KEY,
            trip_id TEXT,
            stop_name TEXT,
            next_stop_name TEXT,
            stop_sequence INT,
            total_passengers INT,
            capacity INT,
            remaining_capacity INT
        );

        CREATE TABLE IF NOT EXISTS segment_demand (
            id SERIAL PRIMARY KEY,
            stop_name TEXT,
            next_stop_name TEXT,
            total_shifted_passengers INT DEFAULT 0
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Tables created.")

def load_csv_to_db():
    conn = connect_db()
    cur = conn.cursor()

    # ✅ Load CSV data
    flights = pd.read_csv("app/data/ROUTE_EMISSIONS_FLIGHTS.csv")
    trains = pd.read_csv("app/data/Final_trains.csv")
    train_trips = pd.read_csv("app/data/trips_with_frequencies.csv")

    # ✅ Insert flights
    for _, row in flights.iterrows():
        cur.execute("""
            INSERT INTO flights (dep_city, des_city, distance, passengers, origin_lat, origin_lon, dest_lat, dest_lon)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (row["dep_city"], row["des_city"], row["Distance"], row["Total Passengers Transported"],
              row["OriginLat"], row["OriginLong"], row["DestLat"], row["DestLong"]))

    # ✅ Insert trains
    for _, row in trains.iterrows():
        cur.execute("""
            INSERT INTO trains (stop_name, next_stop_name, trip_count, total_passengers, capacity, origin_lat, origin_lon, dest_lat, dest_lon)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (row["stop_city"], row["next_stop_city"], row["trip_count"], row["total_passengers"],
              row["capacity"], row["OriginLat"], row["OriginLon"], row["DestLat"], row["DestLon"]))

    # ✅ Insert train trips
    for _, row in train_trips.iterrows():
        cur.execute("""
            INSERT INTO train_trips (trip_id, stop_name, next_stop_name, stop_sequence)
            VALUES (%s, %s, %s, %s);
        """, (row["trip_id"], row["stop_city"], row["next_stop_city"], row["stop_sequence"]))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ CSV data loaded into database.")

# ✅ Run once to set up the database
create_tables()
load_csv_to_db()
