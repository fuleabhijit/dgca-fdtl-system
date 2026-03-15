from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from app.database import Base

class DutyPeriod(Base):
    __tablename__ = "duty_periods"

    id = Column(Integer, primary_key=True, index=True)
    pilot_id = Column(Integer, ForeignKey("pilots.id"))
    duty_start = Column(DateTime)
    duty_end = Column(DateTime)
    duration_hours = Column(Float, nullable=True)  # ← NEW