from fastapi import APIRouter
import pandas as pd
import time

router = APIRouter()

# Load datasets (use actual paths to your CSV files)
FLIGHTS_DATA = "app/data/ROUTE_EMISSIONS_FLIGHTS.csv"
TRAINS_DATA = "app/data/Final_trains.csv"
TRAIN_TRIPS = "app/data/trips_with_frequencies.csv"
#FLIGHTS_DATA = "app/data/dummy_flights.csv"
#TRAIN_TRIPS = "app/data/dummy_train_trips.csv"
# Helper function to load data
def load_data(file_path):
    return pd.read_csv(file_path,low_memory=False)
#trains = load_data(TRAINS_DATA)
#flights = load_data(FLIGHTS_DATA)
# Endpoint: Fetch all flight data
@router.get("/api/flights")
def get_flights():
    flights = load_data(FLIGHTS_DATA)
    return flights.to_dict(orient="records")

@router.get("/api/flights/above/{km}")
def get_flights_above(km: int):
    flights = load_data(FLIGHTS_DATA)
    flightsAbove = flights[flights['Distance'] > km]
    print(f"length of flights above {km} = {len(flightsAbove)}")
    return flightsAbove.to_dict(orient="records")

@router.get("/api/flights/emissions/above/{km}")
def get_flights_above_emissions(km: int):
    flights = load_data(FLIGHTS_DATA)
    flightsAbove = flights[flights['Distance'] > km]
    flightsAboveEmissions = flightsAbove['TotalEmissions'].sum()
    print(f"length of flights above {km} = {len(flightsAbove)}")
    return flightsAboveEmissions

# Endpoint: Fetch all train data
@router.get("/api/trains")
def get_trains():
    trains = load_data(TRAINS_DATA)
    trains = trains[(trains['DestLat'].notnull()) & (trains['DestLon'].notnull()) & (trains['OriginLat'] != "") & (trains['OriginLon'] != "")]
    trains = trains.fillna(value="1.0")
    print(f"train dataset length {len(trains)}")
    processed_trains = [
    {
        "origin": row["stop_name"],
        "destination": row["next_stop_name"],
        "path": [[row["OriginLat"], row["OriginLon"]], [row["DestLat"], row["DestLon"]]],
        "frequency": row["trip_count"],  # Use trip_count as frequency
    }
    for _, row in trains.iterrows()
    ]
    return processed_trains
    #return trains.to_dict(orient="records")
@router.get("/api/trainEmissions/{km}")
def get_train_emissions(km:int):
    trips = load_data(TRAIN_TRIPS)
    if km<200:
        totalemissions = ((trips['Emissions_Per_trip']* trips['adjusted_days_per_year'] / 1000000).sum() * 0.3 )/ 15
        return totalemissions
    elif km<300:
        totalemissions = ((trips['Emissions_Per_trip']* trips['adjusted_days_per_year'] / 1000000).sum() * 0.3 + 1 *3564 )/15
        return totalemissions
    elif km<400:
        totalemissions = ((trips['Emissions_Per_trip']* trips['adjusted_days_per_year'] / 1000000).sum() * 0.3 + 2 *3564 )/15
        return totalemissions
    elif km<500:
        totalemissions = ((trips['Emissions_Per_trip']* trips['adjusted_days_per_year']).sum() * 0.3/ 1000000 + 2.5 *3564 )/15
        return totalemissions
    else :
        totalemissions = ((trips['Emissions_Per_trip']* trips['adjusted_days_per_year'] / 1000000).sum() * 0.3 + 3 *3564 )/15
        return totalemissions
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


# @router.get("/api/replaced_routes/{km}")
# def get_replaced_routes(km: int):
#     flights = load_data(FLIGHTS_DATA)
#     trains = load_data(TRAINS_DATA)
#     trips = load_data(TRAIN_TRIPS)

#     # Filter flights above the specified distance
#     removed_flights = flights[flights['Distance'] < km]

#     result = []
    
#     for _, flight in removed_flights.iterrows():
#         dep_city = flight['dep_city']
#         des_city = flight['des_city']
#         passengers = flight['Total Passengers Transported']

#         # Find train trips that contain both dep_city and des_city
#         possible_trips = trips[
#             (trips["stop_city"] == dep_city) | (trips["next_stop_city"] == dep_city)
#         ].groupby("trip_id").apply(lambda x: set(x["stop_city"]).union(set(x["next_stop_city"])))

#         found_route = False
        
#         for trip_id, stops in possible_trips.items():
#             if dep_city in stops and des_city in stops:
#                 # Get the train segments for this trip
#                 train_segments = trains[trains["trip_id"] == trip_id]

#                 # Check if capacity is sufficient across all segments
#                 sufficient_capacity = all(
#                     row["capacity"] >= passengers for _, row in train_segments.iterrows()
#                 )

#                 color = "orange" if sufficient_capacity else "red"

#                 result.append({
#                     "origin": dep_city,
#                     "destination": des_city,
#                     "path": [[row["OriginLat"], row["OriginLon"]], [row["DestLat"], row["DestLon"]]],
#                     "color": color,
#                 })
                
#                 found_route = True
#                 break  # Stop checking once we find a valid trip

#         if not found_route:
#             # No existing train route, create a new proposed one in red
#             result.append({
#                 "origin": dep_city,
#                 "destination": des_city,
#                 "path": [[flight["OriginLat"], flight["OriginLong"]], [flight["DestLat"], flight["DestLong"]]],
#                 "color": "red"
#             })

#     return result



# @router.get("/api/replaced_routes/{km}")
# def get_replaced_routes(km: int):
#     print("REPLACING ROUTES\n")
#     flights = load_data(FLIGHTS_DATA)
#     trains = load_data(TRAINS_DATA)
#     trips = load_data(TRAIN_TRIPS)

#     result = []
    
#     # Filter flights above the given distance
#     removed_flights = flights[flights['Distance'] < km]

#     for _, flight in removed_flights.iterrows():
#         dep_city = flight['dep_city']
#         des_city = flight['des_city']
#         passengers = flight['Total Passengers Transported']

#         # 🔍 Find trips that contain BOTH dep_city and des_city in `trips_with_frequencies`
#         matching_trips = trips.groupby("trip_id").apply(lambda x: set(x["stop_city"]).union(set(x["next_stop_city"])))

#         found_route = False

#         for trip_id, stops in matching_trips.items():
#             if dep_city in stops and des_city in stops:
#                 # Get all stop segments for this trip
#                 trip_segments = trips[trips["trip_id"] == trip_id][["stop_name", "next_stop_name"]]

#                 # 🚆 Check if all segments exist in Final_trains.csv and have enough capacity
#                 sufficient_capacity = True
#                 train_paths = []

#                 for _, segment in trip_segments.iterrows():
#                     stop_pair = (segment["stop_name"], segment["next_stop_name"])

#                     # Find this segment in `Final_trains.csv`
#                     train_segment = trains[
#                         (trains["stop_name"] == stop_pair[0]) & 
#                         (trains["next_stop_name"] == stop_pair[1])
#                     ]

#                     if train_segment.empty or train_segment["capacity"].iloc[0] < passengers:
#                         sufficient_capacity = False  # 🚨 Capacity insufficient
#                         break  # No need to check further

#                     # Save coordinates for mapping
#                     train_paths.append([[train_segment["OriginLat"].iloc[0], train_segment["OriginLon"].iloc[0]],
#                                         [train_segment["DestLat"].iloc[0], train_segment["DestLon"].iloc[0]]])

#                 # Assign color based on capacity
#                 color = "orange" if sufficient_capacity else "red"

#                 result.append({
#                     "origin": dep_city,
#                     "destination": des_city,
#                     "path": train_paths,
#                     "color": color
#                 })

#                 found_route = True
#                 break  # Stop checking once we find a valid trip

#         if not found_route:
#             # 🚨 No direct train trip found, create a proposed route in red
#             result.append({
#                 "origin": dep_city,
#                 "destination": des_city,
#                 "path": [[flight["OriginLat"], flight["OriginLong"]], [flight["DestLat"], flight["DestLong"]]],
#                 "color": "red"
#             })

#     return result




# def load_data(file_path):
#     return pd.read_csv(file_path, low_memory=False)

# @router.get("/api/replaced_routes/{km}")
# def get_replaced_routes(km: int):
#     start_time = time.time()
#     print("🚆 REPLACING ROUTES STARTED")

#     flights = load_data(FLIGHTS_DATA)
#     trains = load_data(TRAINS_DATA)
#     trips = load_data(TRAIN_TRIPS)

#     print("✅ Data loaded in", round(time.time() - start_time, 2), "seconds")

#     # ✅ Filter flights (O(n))
#     removed_flights = flights[flights["Distance"] < km]
#     print("✅ Filtered flights in", round(time.time() - start_time, 2), "seconds")

#     # ✅ Precompute train segments for fast lookup (O(n))
#     train_dict = {
#         (row["stop_name"], row["next_stop_name"]): row["capacity"]
#         for _, row in trains.iterrows()
#     }

#     # ✅ Precompute trip stop-city mappings (O(n))
#     trip_city_dict = {}

#     for trip_id, row in trips.groupby("trip_id")[["stop_city", "next_stop_city"]].agg(set).iterrows():
#         for stop in row["stop_city"]:
#             trip_city_dict.setdefault(stop, set()).add(trip_id)
#         for next_stop in row["next_stop_city"]:
#             trip_city_dict.setdefault(next_stop, set()).add(trip_id)

#     print("✅ Precomputed trip lookups in", round(time.time() - start_time, 2), "seconds")

#     # ✅ Process flights efficiently
#     result = []
#     for _, flight in removed_flights.iterrows():
#         dep_city = flight['dep_city']
#         des_city = flight['des_city']
#         passengers = flight['Total Passengers Transported']

#         # ✅ Fast lookup using set intersection (O(1))
#         matching_trip_ids = trip_city_dict.get(dep_city, set()) & trip_city_dict.get(des_city, set())

#         if not matching_trip_ids:
#             # No direct train route found
#             result.append({
#                 "origin": dep_city,
#                 "destination": des_city,
#                 "path": [[flight["OriginLat"], flight["OriginLong"]], [flight["DestLat"], flight["DestLong"]]],
#                 "color": "red"
#             })
#             continue

#         found_route = False
#         for trip_id in matching_trip_ids:
#             trip_segments = trips[trips["trip_id"] == trip_id][["stop_name", "next_stop_name"]]
            
#             # ✅ Fast lookup instead of filtering
#             sufficient_capacity = all(
#                 train_dict.get((row["stop_name"], row["next_stop_name"]), 0) >= passengers
#                 for _, row in trip_segments.iterrows()
#             )

#             color = "orange" if sufficient_capacity else "red"

#             result.append({
#                 "origin": dep_city,
#                 "destination": des_city,
#                 "path": [[flight["OriginLat"], flight["OriginLong"]], [flight["DestLat"], flight["DestLong"]]],
#                 "color": color
#             })

#             found_route = True
#             break  # Stop checking once we find a valid train route

#     print("✅ API response generated in", round(time.time() - start_time, 2), "seconds")
#     return result


# @router.get("/api/replaced_routes/{km}")
# def get_replaced_routes(km: int):
#     start_time = time.time()
#     print("🚆 REPLACING ROUTES STARTED")

#     flights = load_data(FLIGHTS_DATA)
#     trains = load_data(TRAINS_DATA)
#     trips = load_data(TRAIN_TRIPS)

#     print("✅ Data loaded in", round(time.time() - start_time, 2), "seconds")

#     # ✅ Filter flights (O(n))
#     removed_flights = flights[flights["Distance"] < km]
#     print("✅ Filtered flights in", round(time.time() - start_time, 2), "seconds")

#     # ✅ Precompute train segments for fast lookup (O(n))
#     train_dict = {
#         (row["stop_name"], row["next_stop_name"]): row
#         for _, row in trains.iterrows()
#     }

#     # ✅ Precompute trip stop-city mappings (O(n))
#     trip_city_dict = {}

#     for trip_id, row in trips.groupby("trip_id")[["stop_city", "next_stop_city"]].agg(set).iterrows():
#         for stop in row["stop_city"]:
#             trip_city_dict.setdefault(stop, set()).add(trip_id)
#         for next_stop in row["next_stop_city"]:
#             trip_city_dict.setdefault(next_stop, set()).add(trip_id)

#     print("✅ Precomputed trip lookups in", round(time.time() - start_time, 2), "seconds")

#     # ✅ Process flights efficiently
#     result = []
#     for _, flight in removed_flights.iterrows():
#         dep_city = flight['dep_city']
#         des_city = flight['des_city']
#         passengers = flight['Total Passengers Transported']

#         # ✅ Fast lookup using set intersection (O(1))
#         matching_trip_ids = trip_city_dict.get(dep_city, set()) & trip_city_dict.get(des_city, set())

#         if not matching_trip_ids:
#             # No direct train route found
#             result.append({
#                 "origin": dep_city,
#                 "destination": des_city,
#                 "segments": [],  # No train route available
#                 "color": "red"
#             })
#             continue

#         found_route = False
#         for trip_id in matching_trip_ids:
#             trip_segments = trips[trips["trip_id"] == trip_id][["stop_name", "next_stop_name"]]

#             segment_paths = []
#             for _, segment in trip_segments.iterrows():
#                 stop_pair = (segment["stop_name"], segment["next_stop_name"])
#                 train_segment = train_dict.get(stop_pair)

#                 if train_segment is None:
#                     continue  # Skip if no segment data

#                 # Get coordinates
#                 segment_path = [
#                     [train_segment["OriginLat"], train_segment["OriginLon"]],
#                     [train_segment["DestLat"], train_segment["DestLon"]]
#                 ]

#                 # Color logic based on capacity
#                 color = "orange" if train_segment["capacity"] >= passengers else "red"

#                 segment_paths.append({
#                     "path": segment_path,
#                     "color": color
#                 })

#             result.append({
#                 "origin": dep_city,
#                 "destination": des_city,
#                 "segments": segment_paths  # ✅ Returning full train segments instead of just dep → des
#             })

#             found_route = True
#             break  # Stop checking once we find a valid train route

#     print("✅ API response generated in", round(time.time() - start_time, 2), "seconds")
#     return result



# #SHA8AL
# @router.get("/api/replaced_routes/{km}")
# def get_replaced_routes(km: int):
#     start_time = time.time()
#     print("🚆 REPLACING ROUTES STARTED")

#     flights = load_data(FLIGHTS_DATA)
#     trains = load_data(TRAINS_DATA)
#     trips = load_data(TRAIN_TRIPS)

#     print("✅ Data loaded in", round(time.time() - start_time, 2), "seconds")

#     # ✅ Filter flights (O(n))
#     removed_flights = flights[flights["Distance"] < km]
#     print("✅ Filtered flights in", round(time.time() - start_time, 2), "seconds")

#     # ✅ Precompute train segments for fast lookup (O(n))
#     train_dict = {
#         (row["stop_name"], row["next_stop_name"]): row
#         for _, row in trains.iterrows()
#     }

#     # ✅ Precompute trip stop-city mappings (O(n))
#     trip_city_dict = {}

#     for trip_id, row in trips.groupby("trip_id")[["stop_city", "next_stop_city"]].agg(set).iterrows():
#         for stop in row["stop_city"]:
#             trip_city_dict.setdefault(stop, set()).add(trip_id)
#         for next_stop in row["next_stop_city"]:
#             trip_city_dict.setdefault(next_stop, set()).add(trip_id)

#     print("✅ Precomputed trip lookups in", round(time.time() - start_time, 2), "seconds")

#     # ✅ Process flights efficiently
#     result = []
#     for _, flight in removed_flights.iterrows():
#         dep_city = flight['dep_city']
#         des_city = flight['des_city']
#         passengers = flight['Total Passengers Transported']

#         # ✅ Fast lookup using set intersection (O(1))
#         matching_trip_ids = trip_city_dict.get(dep_city, set()) & trip_city_dict.get(des_city, set())

#         if not matching_trip_ids:
#             # No direct train route found
#             result.append({
#                 "origin": dep_city,
#                 "destination": des_city,
#                  "segments": [
#                     {
#                         "path": [[flight["OriginLat"], flight["OriginLong"]], [flight["DestLat"], flight["DestLong"]]],
#                         "color": "red"  # 🚨 Mark missing routes in red
#                     }
#                 ]
#             })
#             continue

#         found_route = False
#         for trip_id in matching_trip_ids:
#             trip_segments = trips[trips["trip_id"] == trip_id][["stop_name", "next_stop_name"]]

#             segment_paths = []
#             for _, segment in trip_segments.iterrows():
#                 stop_pair = (segment["stop_name"], segment["next_stop_name"])
#                 train_segment = train_dict.get(stop_pair)

#                 if train_segment is None:
#                     continue  # Skip if no segment data

#                 # Get coordinates
#                 segment_path = [
#                     [train_segment["OriginLat"], train_segment["OriginLon"]],
#                     [train_segment["DestLat"], train_segment["DestLon"]]
#                 ]

#                 # Capacity logic:
#                 current_capacity = train_segment["capacity"]
#                 required_increase = passengers / current_capacity
    

#                 if passengers <= current_capacity:
#                     color = "blue"  # ✅ Train already has enough capacity
                    
#                 elif required_increase < 3:
#                     color = "orange"  # ✅ Needs <3x capacity increase
#                 else:
#                     color = "red"  # 🚨 Needs 3x+ capacity increase

#                 segment_paths.append({
#                     "path": segment_path,
#                     "color": color
#                 })

#             result.append({
#                 "origin": dep_city,
#                 "destination": des_city,
#                 "segments": segment_paths  # ✅ Returning full train segments with capacity colors
#             })

#             found_route = True
#             break  # Stop checking once we find a valid train route

#     print("✅ API response generated in", round(time.time() - start_time, 2), "seconds")
#     return result


# from collections import defaultdict
# import json
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.database import SessionLocal
# from app.models import Flight, Train, TrainTrip, SegmentDemand

# #router = APIRouter()

# # ✅ Get database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.get("/api/replaced_routes/{km}")
# def get_replaced_routes(km: int, db: Session = Depends(get_db)):
#     start_time = time.time()
#     print("🚆 REPLACING ROUTES STARTED")

#     # ✅ Get removed flights from database
#     start = time.time()
#     flights = db.query(Flight).filter(Flight.distance < km).all()
#     print(f"Time to query filtered flights: {time.time()-start}\n")

#     # ✅ Compute demand shifts
#     segment_demand = {}

#     for flight in flights:
#         print(f"Flight ID: {flight.id}, From: {flight.dep_city}, To: {flight.des_city}, Distance: {flight.distance}, Passengers: {flight.passengers}")

#         # ✅ Find train trips that contain both dep_city and des_city in their route
#         matching_trips = (
#             db.query(TrainTrip)
#             .filter(TrainTrip.route.contains(flight.dep_city), TrainTrip.route.contains(flight.des_city))
#             .all()
#         )
#         print(f"Number of matching trips: {len(matching_trips)}\n")
#         for trip in matching_trips:
#             route_stops = trip.route  # List of stops (already ordered)

#             if flight.dep_city in route_stops and flight.des_city in route_stops:
#                 dep_index = route_stops.index(flight.dep_city)
#                 des_index = route_stops.index(flight.des_city)

#                 if dep_index < des_index:  # Ensure correct order
#                     segment_pairs = [
#                         (route_stops[i], route_stops[i + 1])
#                         for i in range(dep_index, des_index)
#                     ]

#                     for segment in segment_pairs:
#                         segment_demand[segment] = segment_demand.get(segment, 0) + flight.passengers

#     # ✅ Compute response
#     result = []
#     start = time.time()
#     trains = db.query(Train).all()

#     for train in trains:
#         stop_pair = (train.stop_name, train.next_stop_name)
#         total_passengers = segment_demand.get(stop_pair, 0) + train.total_passengers
#         capacity = train.capacity

#         required_increase = total_passengers / capacity if capacity > 0 else 99999
#         color = "blue" if total_passengers <= capacity else "orange" if required_increase < 3 else "red"

#         result.append({
#             "path": [[train.origin_lat, train.origin_lon], [train.dest_lat, train.dest_lon]],
#             "color": color
#         })

#     print(f"time updating train trips: {time.time() - start}\n")
#     print("✅ API response generated in", round(time.time() - start_time, 2), "seconds")
#     return result

import numpy as np
#Sha8al bardo
# @router.get("/api/replaced_routes/{km}")
# def get_replaced_routes(km: int):
#     start_time = time.time()
#     print("🚆 REPLACING ROUTES STARTED")

#     # ✅ Load datasets
#     flights = load_data(FLIGHTS_DATA)
#     trains = load_data(TRAINS_DATA)
#     trips = load_data(TRAIN_TRIPS)

#     print("✅ Data loaded in", round(time.time() - start_time, 2), "seconds")

#     # ✅ Filter flights that are removed (O(n))
#     removed_flights = flights[flights["Distance"] < km]
#     print("✅ Filtered flights in", round(time.time() - start_time, 2), "seconds")

#     # ✅ Precompute trip stop-city mappings (O(n))
#     trip_city_dict = {}
#     for trip_id, row in trips.groupby("trip_id")[["stop_city", "next_stop_city"]].agg(set).iterrows():
#         for stop in row["stop_city"]:
#             trip_city_dict.setdefault(stop, set()).add(trip_id)
#         for next_stop in row["next_stop_city"]:
#             trip_city_dict.setdefault(next_stop, set()).add(trip_id)

#     # ✅ Store remaining capacity for each trip (O(n))
#     trip_capacity = {row["trip_id"]: row["trip_capacity"] for _, row in trips.iterrows()}

#     print("✅ Precomputed trip lookups in", round(time.time() - start_time, 2), "seconds")

#     # ✅ Process flights efficiently
#     result = []

#     for _, flight in removed_flights.iterrows():
#         dep_city = flight["dep_city"]
#         des_city = flight["des_city"]
#         passengers = flight["Total Passengers Transported"]

#         # ✅ Find matching train trips (O(1))
#         matching_trip_ids = trip_city_dict.get(dep_city, set()) & trip_city_dict.get(des_city, set())
#         print(f"matching_trip_ids: {matching_trip_ids}\n")
#         if not matching_trip_ids:
#             # ❌ No direct train route found, mark in red
#             result.append({
#                 "origin": dep_city,
#                 "destination": des_city,
#                 "segments": [{
#                     "path": [[flight["OriginLat"], flight["OriginLong"]], [flight["DestLat"], flight["DestLong"]]],
#                     "color": "red"
#                 }]
#             })
#             continue

#         # ✅ Distribute passengers among multiple trips
#         remaining_passengers = passengers
#         successful_trips = []

#         for trip_id in matching_trip_ids:
#             print(f"Iterating through trip with trip ID: {trip_id}\n")
#             if remaining_passengers <= 0:
#                 break  # Stop once all passengers are assigned

#             # ✅ Get trip data
#             trip_segments = trips[trips["trip_id"] == trip_id][["stop_name", "next_stop_name", "OriginLat", "OriginLon", "DestLat", "DestLon"]]
#             trip_capacity_left = trip_capacity.get(trip_id, 0)

#             # ✅ Ensure all segments have enough capacity
#             all_segments_have_capacity = trip_capacity_left >= remaining_passengers
#             segment_paths = []

#             for _, segment in trip_segments.iterrows():
#                 # ✅ Ensure no NaN values
#                 origin_lat = segment["OriginLat"]
#                 origin_lon = segment["OriginLon"]
#                 dest_lat = segment["DestLat"]
#                 dest_lon = segment["DestLon"]

#                 if np.isnan(origin_lat) or np.isnan(origin_lon) or np.isnan(dest_lat) or np.isnan(dest_lon):
#                     continue  # Skip segments with invalid coordinates

#                 segment_path = [[origin_lat, origin_lon], [dest_lat, dest_lon]]

#                 if all_segments_have_capacity:
#                     color = "blue"  # ✅ Sufficient capacity
#                     trip_capacity[trip_id] -= remaining_passengers  # ✅ Update capacity
#                     remaining_passengers = 0
#                 else:
#                     color = "orange"  # 🚨 Needs upgrade

#                 segment_paths.append({"path": segment_path, "color": color})

#             if segment_paths:
#                 successful_trips.append(segment_paths)

#         # ✅ If passengers are successfully reassigned, add the trip to the result
#         if successful_trips:
#             result.append({
#                 "origin": dep_city,
#                 "destination": des_city,
#                 "segments": successful_trips[0]  # ✅ Add trip segments
#             })
#         else:
#             # ❌ If no trip could take all passengers, mark segments in orange
#             for trip_id in matching_trip_ids:
#                 trip_segments = trips[trips["trip_id"] == trip_id][["stop_name", "next_stop_name", "OriginLat", "OriginLon", "DestLat", "DestLon"]]
#                 segment_paths = []

#                 for _, segment in trip_segments.iterrows():
#                     # ✅ Ensure no NaN values
#                     origin_lat = segment["OriginLat"]
#                     origin_lon = segment["OriginLon"]
#                     dest_lat = segment["DestLat"]
#                     dest_lon = segment["DestLon"]

#                     if np.isnan(origin_lat) or np.isnan(origin_lon) or np.isnan(dest_lat) or np.isnan(dest_lon):
#                         continue  # Skip segments with invalid coordinates

#                     segment_path = [[origin_lat, origin_lon], [dest_lat, dest_lon]]
#                     segment_paths.append({"path": segment_path, "color": "orange"})  # 🚨 Needs upgrade

#                 if segment_paths:
#                     result.append({
#                         "origin": dep_city,
#                         "destination": des_city,
#                         "segments": segment_paths
#                     })

#     print("✅ API response generated in", round(time.time() - start_time, 2), "seconds")
#     return result

import numpy as np
# @router.get("/api/replaced_routes/{km}")
# def get_replaced_routes(km: int):
#     start_time = time.time()
#     print("🚆 REPLACING ROUTES STARTED")

#     # ✅ Load datasets
#     flights = load_data(FLIGHTS_DATA)
#     trains = load_data(TRAINS_DATA)
#     trips = load_data(TRAIN_TRIPS)

#     print("✅ Data loaded in", round(time.time() - start_time, 2), "seconds")

#     # ✅ Filter flights that are removed (O(n))
#     removed_flights = flights[flights["Distance"] < km]
#     print("✅ Filtered flights in", round(time.time() - start_time, 2), "seconds")

#     # ✅ Precompute trip stop-city mappings (O(n))
#     trip_city_dict = {}
#     for trip_id, row in trips.groupby("trip_id")[["stop_city", "next_stop_city"]].agg(set).iterrows():
#         for stop in row["stop_city"]:
#             trip_city_dict.setdefault(stop, set()).add(trip_id)
#         for next_stop in row["next_stop_city"]:
#             trip_city_dict.setdefault(next_stop, set()).add(trip_id)

#     # ✅ Store remaining capacity for each trip (O(n))
#     trip_capacity = {row["trip_id"]: row["trip_passengers_transporter_per_year"] for _, row in trips.iterrows()}

#     print("✅ Precomputed trip lookups in", round(time.time() - start_time, 2), "seconds")

#     # ✅ Process flights efficiently
#     result = []

#     for _, flight in removed_flights.iterrows():
#         dep_city = flight["dep_city"]
#         des_city = flight["des_city"]
#         passengers = flight["Total Passengers Transported"]

#         # ✅ Find matching train trips that have a direct route from dep_city to des_city (O(1))
#         matching_trip_ids = set()
#         for trip_id in trip_city_dict.get(dep_city, set()):
#             if trip_id in trip_city_dict.get(des_city, set()):
#                 matching_trip_ids.add(trip_id)
#         matching_trip_ids = trip_city_dict.get(dep_city, set()) & trip_city_dict.get(des_city, set())

#         print(f"matchin trips: {matching_trip_ids}\n")
#         if not matching_trip_ids:
#             # ❌ No direct train route found, mark in red
#             result.append({
#                 "origin": dep_city,
#                 "destination": des_city,
#                 "segments": [{
#                     "path": [[flight["OriginLat"], flight["OriginLong"]], [flight["DestLat"], flight["DestLong"]]],
#                     "color": "red"
#                 }]
#             })
#             continue

#         # ✅ Compute total available capacity across all trips
#         total_available_capacity = sum(trip_capacity[trip_id] for trip_id in matching_trip_ids)
#         print(f"total available capacity for all trips for removed flight: {total_available_capacity}\n")
#         if total_available_capacity < passengers:
#             print(f"total available capacity is less than passengers transported from flight({passengers})\n")

#             # 🚨 Not enough space across all trips, mark segments in orange
#             for trip_id in matching_trip_ids:
#                 trip_segments = trips[(trips["trip_id"] == trip_id) & 
#                                       (trips["stop_name"] == dep_city) | 
#                                       (trips["next_stop_name"] == des_city)]
#                 segment_paths = []

#                 for _, segment in trip_segments.iterrows():
#                     if any(pd.isna([segment["OriginLat"], segment["OriginLon"], segment["DestLat"], segment["DestLon"]])):
#                         continue

#                     segment_path = [[segment["OriginLat"], segment["OriginLon"]], [segment["DestLat"], segment["DestLon"]]]
#                     segment_paths.append({"path": segment_path, "color": "orange"})  # 🚨 Needs upgrade

#                 if segment_paths:
#                     result.append({
#                         "origin": dep_city,
#                         "destination": des_city,
#                         "segments": segment_paths
#                     })
#             continue

#         # ✅ Distribute passengers among multiple trips proportionally
#         remaining_passengers = passengers
#         successful_trips = []

#         for trip_id in sorted(matching_trip_ids, key=lambda tid: trip_capacity[tid], reverse=True):  # Prioritize higher capacity trips
#             if remaining_passengers <= 0:
#                 break  # Stop once all passengers are assigned
#             trip_segments = trips[(trips["trip_id"] == trip_id) & 
#                                   (trips["stop_city"] == dep_city) | 
#                                   (trips["next_stop_city"] == des_city)]
#             trip_capacity_left = trip_capacity.get(trip_id, 0)
#             assigned_passengers = min(remaining_passengers, trip_capacity_left)
#             trip_capacity[trip_id] -= assigned_passengers  # ✅ Update capacity
#             remaining_passengers -= assigned_passengers
#             print(f"Trip segments: {trip_segments}\n")
#             print(f"Trip capacities : {trip_capacity}\n")
#             segment_paths = []
#             for _, segment in trip_segments.iterrows():
#                 if any(pd.isna([segment["OriginLat"], segment["OriginLon"], segment["DestLat"], segment["DestLon"]])):
#                     continue
#                 segment_path = [[segment["OriginLat"], segment["OriginLon"]], [segment["DestLat"], segment["DestLon"]]]
#                 segment_paths.append({"path": segment_path, "color": "blue"})  # ✅ Sufficient capacity

#             if segment_paths:
#                 print(f"added segment {segment_paths}\n")
#                 successful_trips.append(segment_paths)

#         # ✅ If passengers are successfully reassigned, add the trip to the result
#         if successful_trips:
#             result.append({
#                 "origin": dep_city,
#                 "destination": des_city,
#                 "segments": successful_trips[0]  # ✅ Add trip segments
#             })

#     print("✅ API response generated in", round(time.time() - start_time, 2), "seconds")
#     return result

# Running the function with a test case

#Re-import necessary libraries after execution state reset
#Sha8al bas bati2
@router.get("/api/replaced_routes/{km}")
def get_replaced_routes(km: int):
    start_time = time.time()
    #print("\n🚆 REPLACING ROUTES STARTED")

    # ✅ Load datasets
    flights = load_data(FLIGHTS_DATA)
    trains = load_data(TRAINS_DATA)
    trips = load_data(TRAIN_TRIPS)

    print("✅ Data loaded in", round(time.time() - start_time, 2), "seconds")

    # ✅ Filter flights that are removed (O(n))
    removed_flights = flights[flights["Distance"] < km]
    print("✅ Filtered flights in", round(time.time() - start_time, 2), "seconds")

    # ✅ Precompute trip stop-city mappings (O(n))
    trip_city_dict = {}
    for trip_id, row in trips.groupby("trip_id")[["stop_city", "next_stop_city"]].agg(set).iterrows():
        for stop in row["stop_city"]:
            trip_city_dict.setdefault(stop, set()).add(trip_id)
        for next_stop in row["next_stop_city"]:
            trip_city_dict.setdefault(next_stop, set()).add(trip_id)

    # ✅ Store remaining capacity per segment (O(n))
    segment_capacity = {}
    for _, row in trips.iterrows():
        segment_capacity[(row["trip_id"], row["stop_name"], row["next_stop_name"])] = row["trip_passengers_transporter_per_year"]
    #print(f"segment capacity is {segment_capacity}\n")
    print("✅ Precomputed trip lookups in", round(time.time() - start_time, 2), "seconds")

    # ✅ Process flights efficiently
    result = []

    for _, flight in removed_flights.iterrows():
        dep_city = flight["dep_city"]
        des_city = flight["des_city"]
        passengers = flight["Total Passengers Transported"]

        print(f"🔍 Processing flight from {dep_city} to {des_city} with {passengers} passengers")

        # ✅ Find matching train trips that pass through dep_city to des_city
        matching_trip_ids = set()
        for trip_id in trip_city_dict.get(dep_city, set()):
            if trip_id in trip_city_dict.get(des_city, set()):
                matching_trip_ids.add(trip_id)

        print(f"📍 Matching trips for {dep_city} to {des_city}: {matching_trip_ids}")

        if not matching_trip_ids:
            print(f"❌ No matching trips found for {dep_city} → {des_city}, marking in red\n")
            result.append({
                "origin": dep_city,
                "destination": des_city,
                "segments": [{
                    "path": [[flight["OriginLat"], flight["OriginLong"]], [flight["DestLat"], flight["DestLong"]]],
                    "color": "red"
                }]
            })
            continue
        
        # ✅ Try distributing passengers into available trips
        remaining_passengers = passengers
        successful_trips = []
        segment_paths = []

        for trip_id in sorted(matching_trip_ids, key=lambda tid: sum(trips[trips["trip_id"] == tid]["trip_passengers_transporter_per_year"]), reverse=True):  # Prioritize higher capacity trips
            if remaining_passengers<=0:
                print(f"No remaining passengers left. Reached Trip id {trip_id}\n")
                break
                    # ✅ Find where the route starts and ends within the trip
            relevant_segments = trips[(trips["trip_id"] == trip_id)]
            dep_index = relevant_segments.index[relevant_segments["stop_city"] == dep_city].tolist()
            des_index = relevant_segments.index[relevant_segments["next_stop_city"] == des_city].tolist()
            #print(f"dep index: {dep_index}\n")
            #print(f"dep index: {des_index}\n")
            if dep_index and des_index:
                dep_index = dep_index[0]
                des_index = des_index[-1]

                # ✅ Extract the full route between dep_city and des_city
                trip_segments = relevant_segments.loc[dep_index:des_index]
            else:
                trip_segments = pd.DataFrame()  # No valid route found
            
            bottleneck_capacity = trip_segments["trip_passengers_transporter_per_year"].min() if not trip_segments.empty else 0
            #trip_segments = trips[(trips["trip_id"] == trip_id) ]
            #&                                  ((trips["stop_city"] == dep_city) | (trips["next_stop_city"] == des_city))]
            #print(f"trip segments for trip id: {trip_id} : {trip_segments}\n")
            assigned_passengers = min(remaining_passengers, bottleneck_capacity)


            # ✅ Reduce capacity per **segment**, not entire trip
            for _, segment in trip_segments.iterrows():
                segment_key = (trip_id, segment["stop_name"], segment["next_stop_name"])
                if segment_key in segment_capacity:
                    segment_capacity[segment_key] -= assigned_passengers

            remaining_passengers -= assigned_passengers

            for _, segment in trip_segments.iterrows():
                if any(pd.isna([segment["OriginLat"], segment["OriginLon"], segment["DestLat"], segment["DestLon"]])):
                    continue
                segment_path = [[segment["OriginLat"], segment["OriginLon"]], [segment["DestLat"], segment["DestLon"]]]
                segment_paths.append({"path": segment_path, "color": "blue"})  # ✅ Sufficient capacity


        if remaining_passengers == 0:

            result.append({
                "origin": dep_city,
                "destination": des_city,
                "segments": [{"path": seg["path"], "color": "blue"} for seg in segment_paths]  # ✅ Mark as "blue"
            })
        elif remaining_passengers > 0 and assigned_passengers > 0:
      

            result.append({
                "origin": dep_city,
                "destination": des_city,
                "segments": [{"path": seg["path"], "color": "orange"} for seg in segment_paths]
            })
  
    return result

# import math
# from collections import defaultdict
# @router.get("/api/replaced_routes/{km}")
# def get_replaced_routes(km: int):
#     start_time = time.time()

#     # ✅ Load datasets
#     flights = load_data(FLIGHTS_DATA)
#     trips = load_data(TRAIN_TRIPS)

#     # ✅ Precompute segment-to-trip mapping
#     segment_trip_map = defaultdict(set)
#     trip_segments_map = defaultdict(list)
#     trip_bottleneck_capacity = {}

#     for _, row in trips.iterrows():
#         segment_trip_map[(row["stop_city"], row["next_stop_city"])].add(row["trip_id"])
#         trip_segments_map[row["trip_id"]].append(row)

#     # ✅ Precompute bottleneck capacities
#     for trip_id, segments in trip_segments_map.items():
#         trip_bottleneck_capacity[trip_id] = min(seg["trip_passengers_transporter_per_year"] for seg in segments)

#     # ✅ Filter removed flights
#     removed_flights = flights[flights["Distance"] < km]

#     # ✅ Process flights efficiently
#     result = []
#     for _, flight in removed_flights.iterrows():
#         dep_city, des_city, passengers = flight["dep_city"], flight["des_city"], flight["Total Passengers Transported"]

#         # ✅ Use precomputed segment trip lookup
#         matching_trip_ids = segment_trip_map.get((dep_city, des_city), set())

#         if not matching_trip_ids:
#             result.append({
#                 "origin": dep_city, "destination": des_city,
#                 "segments": [{"path": [[flight["OriginLat"], flight["OriginLong"]],
#                                        [flight["DestLat"], flight["DestLong"]]], "color": "red"}]
#             })
#             continue

#         # ✅ Distribute passengers
#         remaining_passengers = passengers
#         segment_paths = []

#         for trip_id in sorted(matching_trip_ids, key=lambda tid: trip_bottleneck_capacity[tid], reverse=True):
#             if remaining_passengers <= 0:
#                 break

#             trip_segments = trip_segments_map[trip_id]
#             assigned_passengers = min(remaining_passengers, trip_bottleneck_capacity[trip_id])

#             for segment in trip_segments:
#                 if any(pd.isna([segment["OriginLat"], segment["OriginLon"], segment["DestLat"], segment["DestLon"]])):
#                     #print(f"⚠️ Skipping segment due to NaN values: {segment}")
#                     continue  # Skip segments with NaN values

#                 segment_paths.append({
#                     "path": [[segment["OriginLat"], segment["OriginLon"]],
#                              [segment["DestLat"], segment["DestLon"]]],
#                     "color": "blue" if assigned_passengers > 0 else "orange"
#                 })

#             remaining_passengers -= assigned_passengers

#         if remaining_passengers == 0:
#             result.append({"origin": dep_city, "destination": des_city, "segments": segment_paths})
#         elif assigned_passengers > 0:
#             result.append({"origin": dep_city, "destination": des_city, "segments": [{"path": seg["path"], "color": "orange"} for seg in segment_paths]})

#     # ✅ Debug: Check for NaN values before returning
#     # for entry in result:
#     #     for segment in entry["segments"]:
#     #         for coord in segment["path"]:
#     #             if any(math.isnan(c) for c in coord):
#     #                 print(f"❌ NaN Detected in Path: {segment['path']}")

#     return result
