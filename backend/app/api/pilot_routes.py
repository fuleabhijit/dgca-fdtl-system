from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.pilot import Pilot

router = APIRouter(prefix="/pilots", tags=["Pilots"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_pilot(name: str, employee_id: str, db: Session = Depends(get_db)):
    pilot = Pilot(name=name, employee_id=employee_id)
    db.add(pilot)
    db.commit()
    db.refresh(pilot)   # ← this was missing — loads the saved object back from DB
    return pilot


@router.get("/")
def get_pilots(db: Session = Depends(get_db)):
    return db.query(Pilot).all()