from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://abhijitfule@localhost:5432/fdtl_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Register models
import backend.app.models.pilot
import backend.app.models.flight
import backend.app.models.duty_period
import backend.app.models.rest_period
import backend.app.models.pilot_flight
import backend.app.models.violation
import backend.app.models.audit_log