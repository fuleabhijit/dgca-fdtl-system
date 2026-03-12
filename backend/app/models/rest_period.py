from sqlalchemy import Column, Integer, DateTime, ForeignKey
from backend.app.database import Base

class RestPeriod(Base):

    __tablename__ = "rest_periods"

    id = Column(Integer, primary_key=True, index=True)

    pilot_id = Column(Integer, ForeignKey("pilots.id"))

    rest_start = Column(DateTime)

    rest_end = Column(DateTime)