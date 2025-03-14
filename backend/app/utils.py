import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Flight, Train, TrainTrip
def clean_value(value, default="Unknown"):
    """ Ensures no NaN values are inserted into the database """
    return default if pd.isna(value) else value
def load_csv_to_db():
    db: Session = SessionLocal()

    # ✅ Load CSV files
    flights = pd.read_csv("./data/ROUTE_EMISSIONS_FLIGHTS.csv")
    trains = pd.read_csv("./data/Final_trains.csv")
    train_trips = pd.read_csv("./data/trips_with_frequencies.csv")

    # ✅ Insert Flights
    for _, row in flights.iterrows():
        flight = Flight(
            dep_city=row["dep_city"],
            des_city=row["des_city"],
            distance=row["Distance"],
            passengers=row["Total Passengers Transported"],
            origin_lat=row["OriginLat"],
            origin_lon=row["OriginLong"],
            dest_lat=row["DestLat"],
            dest_lon=row["DestLong"],
        )
        db.add(flight)

    # ✅ Insert Trains
    for _, row in trains.iterrows():
        train = Train(
            stop_name=row["stop_name"],
            next_stop_name=row["next_stop_name"],
            trip_count=row["trip_count"],
            total_passengers=row["total_passengers"],
            capacity=row["capacity"],
            origin_lat=row["OriginLat"],
            origin_lon=row["OriginLon"],
            dest_lat=row["DestLat"],
            dest_lon=row["DestLon"],
        )
        db.add(train)

    # ✅ Insert Train Trips
    for _, row in train_trips.iterrows():
        train_trip = TrainTrip(
            trip_id=str(row["trip_id"]),
            stop_name=clean_value(row["stop_name"]),
            next_stop_name=clean_value(row["next_stop_name"]),
            stop_sequence=int(row["stop_sequence"]) if pd.notna(row["stop_sequence"]) else 0  # ✅ Convert to Integer
        )
        db.add(train_trip)

    db.commit()
    db.close()
    print("✅ CSV data loaded into PostgreSQL.")
from collections import defaultdict
from sqlalchemy.orm import Session

def reconstruct_routes(db: Session):
    db: Session = SessionLocal()

    # ✅ Step 1: Fetch all train segments
    train_segments = db.query(TrainTrip.train_id, TrainTrip.stop_name, TrainTrip.next_stop_name).all()

    # ✅ Step 2: Group by train_id
    routes_map = defaultdict(dict)  # {train_id: {stop_name: next_stop_name}}
    all_stops = defaultdict(set)    # {train_id: set(all_stops)}
    
    for train_id, stop, next_stop in train_segments:
        routes_map[train_id][stop] = next_stop
        all_stops[train_id].add(stop)
        all_stops[train_id].add(next_stop)

    # ✅ Step 3: Identify starting stops
    full_routes = {}
    for train_id, segments in routes_map.items():
        possible_starts = all_stops[train_id] - set(segments.values())  # Stops that are never "next_stop"
        if not possible_starts:
            raise ValueError(f"Cycle detected in train {train_id}, cannot reconstruct route.")
        
        start_stop = possible_starts.pop()  # Pick the first valid starting stop
        route = [start_stop]

        # ✅ Step 4: Reconstruct the ordered route
        while start_stop in segments:
            next_stop = segments[start_stop]
            route.append(next_stop)
            start_stop = next_stop  # Move to the next stop
        
        full_routes[train_id] = route

    # ✅ Step 5: Update database with full routes
    for train_id, route_list in full_routes.items():
        db.query(TrainTrip).filter(TrainTrip.train_id == train_id).update({"route": route_list})
    
    db.commit()
    print("✅ Train routes populated successfully!")


# ✅ Run once to insert data into the database
if __name__ == "__main__":
    load_csv_to_db()
    reconstruct_routes()
