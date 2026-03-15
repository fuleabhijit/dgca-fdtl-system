from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import SessionLocal
from app.models.duty_period import DutyPeriod
from app.services.rule_engine import check_duty_period
from app.utils.time_utils import calculate_hours

router = APIRouter(prefix="/duty", tags=["Duty"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE DUTY RECORD
@router.post("/")
def create_duty(
    pilot_id: int,
    duty_start: datetime,
    duty_end: datetime,
    db: Session = Depends(get_db)
):
    duration = calculate_hours(duty_start, duty_end)

    duty = DutyPeriod(
        pilot_id=pilot_id,
        duty_start=duty_start,
        duty_end=duty_end,
        duration_hours=round(duration, 2)
    )

    db.add(duty)
    db.commit()
    db.refresh(duty)

    # Run rule engine after saving
    check_duty_period(
        db,
        pilot_id=pilot_id,
        duty_start=duty_start,
        duty_end=duty_end
    )

    return duty


# GET ALL DUTY RECORDS
@router.get("/")
def get_duty_records(db: Session = Depends(get_db)):
    return db.query(DutyPeriod).all()