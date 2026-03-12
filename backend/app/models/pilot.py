from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from backend.app.database import Base

class Pilot(Base):

    __tablename__ = "pilots"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(String, unique=True, nullable=False)

    name = Column(String, nullable=False)

    rank = Column(String)

    base_airport = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)