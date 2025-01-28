from fastapi import APIRouter
import pandas as pd

router = APIRouter()

# Load datasets (use actual paths to your CSV files)
FLIGHTS_DATA = "app/data/flights.csv"
TRAINS_DATA = "app/data/train_unique_routes.csv"

# Helper function to load data
def load_data(file_path):
    return pd.read_csv(file_path)
#trains = load_data(TRAINS_DATA)
#flights = load_data(FLIGHTS_DATA)
# Endpoint: Fetch all flight data
@router.get("/api/flights")
def get_flights():
    flights = load_data(FLIGHTS_DATA)
    return flights.to_dict(orient="records")

# Endpoint: Fetch all train data
@router.get("/api/trains")
def get_trains():
    trains = load_data(TRAINS_DATA)
    trains = trains[(trains['DestLat'].notnull()) & (trains['DestLon'].notnull()) & (trains['OriginLat'] != "") & (trains['OriginLon'] != "")]
    trains = trains.fillna(value="1.0")
    print(f"train dataset length {len(trains)}")
    
    return trains.to_dict(orient="records")
@router.get("/api/trainEmissions")
def get_train_emissions():
    trains['emissions']
# Endpoint: Filter flight data by origin and destination
@router.get("/api/flights/search")
def search_flights(origin: str, destination: str):
    flights = load_data(FLIGHTS_DATA)
    filtered = flights[
        (flights["origin"] == origin) & (flights["destination"] == destination)
    ]
    return filtered.to_dict(orient="records")

# Endpoint: Filter train data by origin and destination
@router.get("/api/trains/search")
def search_trains(origin: str, destination: str):
    trains = load_data(TRAINS_DATA)
    filtered = trains[
        (trains["origin"] == origin) & (trains["destination"] == destination)
    ]
    return filtered.to_dict(orient="records")
