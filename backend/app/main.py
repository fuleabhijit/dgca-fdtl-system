from fastapi import FastAPI
from app.database import engine, Base

import app.models.pilot
import app.models.flight
import app.models.duty_period
import app.models.rest_period
import app.models.pilot_flight
import app.models.violation
import app.models.audit_log
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "DGCA FDTL system running"}