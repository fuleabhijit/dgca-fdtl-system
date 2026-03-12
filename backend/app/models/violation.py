from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from app.database import Base


class Violation(Base):

    __tablename__ = "violations"

    id = Column(Integer, primary_key=True)

    pilot_id = Column(Integer, ForeignKey("pilots.id"))

    violation_type = Column(String)

    description = Column(String)

    severity = Column(String)

    resolved = Column(Boolean, default=False)

    detected_at = Column(DateTime, default=datetime.utcnow)