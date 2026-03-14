from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.violation import Violation

router = APIRouter(prefix="/violations", tags=["Violations"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_violations(db: Session = Depends(get_db)):
    return db.query(Violation).all()