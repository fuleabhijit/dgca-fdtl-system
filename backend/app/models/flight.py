from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class Flight(Base):

    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)

    flight_number = Column(String)

    departure_airport = Column(String)

    arrival_airport = Column(String)

    departure_time = Column(DateTime)

    arrival_time = Column(DateTime)

    aircraft_type = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)