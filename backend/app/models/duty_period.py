from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class DutyPeriod(Base):

    __tablename__ = "duty_periods"

    id = Column(Integer, primary_key=True, index=True)

    pilot_id = Column(Integer, ForeignKey("pilots.id"))

    duty_start = Column(DateTime)

    duty_end = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)