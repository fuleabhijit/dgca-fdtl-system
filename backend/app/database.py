import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://abhijitfule@localhost:5432/fdtl_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Register models
import app.models.pilot
import app.models.flight
import app.models.duty_period
import app.models.rest_period
import app.models.pilot_flight
import app.models.violation
import app.models.audit_log