from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, JSON
from sqlalchemy.orm import relationship,declarative_base
from app.database import Base
# ✅ Flight Table
class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    dep_city = Column(String, index=True)
    des_city = Column(String, index=True)
    distance = Column(Float)
    passengers = Column(Integer)
    origin_lat = Column(Float)
    origin_lon = Column(Float)
    dest_lat = Column(Float)
    dest_lon = Column(Float)

# ✅ Train Table
class Train(Base):
    __tablename__ = "trains"

    id = Column(Integer, primary_key=True, index=True)
    stop_name = Column(String, index=True)
    next_stop_name = Column(String, index=True)
    trip_count = Column(Integer)
    total_passengers = Column(Integer)
    capacity = Column(Integer)
    origin_lat = Column(Float)
    origin_lon = Column(Float)
    dest_lat = Column(Float)
    dest_lon = Column(Float)

# ✅ Train Trips Table
class TrainTrip(Base):
    __tablename__ = "train_trips"

    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, index=True)
    route = Column(JSON, nullable=True)  # New column
    total_passengers = Column(Integer, default=0)
    capacity = Column(Integer, default=0)
    remaining_capacity = Column(Integer, default=0)

# ✅ Segment Demand Table
class SegmentDemand(Base):
    __tablename__ = "segment_demand"

    id = Column(Integer, primary_key=True, index=True)
    stop_name = Column(String, index=True)
    next_stop_name = Column(String, index=True)
    total_shifted_passengers = Column(Integer, default=0)
