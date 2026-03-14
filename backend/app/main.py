from fastapi import FastAPI
from app.database import engine, Base

import app.models.pilot
import app.models.flight
import app.models.duty_period
import app.models.rest_period
import app.models.pilot_flight
import app.models.violation
import app.models.audit_log

from app.api import pilot_routes, duty_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(pilot_routes.router)
app.include_router(duty_routes.router)

@app.get("/")
def root():
    return {"message": "DGCA FDTL system running"}