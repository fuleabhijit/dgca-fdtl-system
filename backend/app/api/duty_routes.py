from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import SessionLocal
from app.models.duty_period import DutyPeriod
from app.services.rule_engine import check_duty_period

router = APIRouter(prefix="/duty", tags=["Duty"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_duty(
    pilot_id: int,
    duty_start: datetime,
    duty_end: datetime,
    db: Session = Depends(get_db)
):

    duty = DutyPeriod(
        pilot_id=pilot_id,
        duty_start=duty_start,
        duty_end=duty_end
    )

    db.add(duty)
    db.commit()

    check_duty_period(db, pilot_id, duty_start, duty_end)

    return duty