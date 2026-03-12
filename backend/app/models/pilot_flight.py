from sqlalchemy import Column, Integer, ForeignKey
from backend.app.database import Base

class PilotFlight(Base):

    __tablename__ = "pilot_flights"

    id = Column(Integer, primary_key=True)

    pilot_id = Column(Integer, ForeignKey("pilots.id"))

    flight_id = Column(Integer, ForeignKey("flights.id"))

    duty_period_id = Column(Integer, ForeignKey("duty_periods.id"))