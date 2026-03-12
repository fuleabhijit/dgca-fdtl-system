from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from app.database import Base


class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)

    action = Column(String)

    user_id = Column(String)

    details = Column(JSON)

    timestamp = Column(DateTime, default=datetime.utcnow)