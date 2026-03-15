from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import SessionLocal
from app.models.violation import Violation
from app.models.pilot import Pilot
from app.services.groq_service import explain_violation

router = APIRouter(prefix="/violations", tags=["Violations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET ALL VIOLATIONS (with optional filters)
@router.get("/")
def get_violations(
    severity: Optional[str] = Query(None, description="Filter by: HIGH, MEDIUM, LOW"),
    pilot_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Violation)

    if severity:
        query = query.filter(Violation.severity == severity.upper())

    if pilot_id:
        query = query.filter(Violation.pilot_id == pilot_id)

    return query.order_by(Violation.id.desc()).all()


# GET AI EXPLANATION FOR A SPECIFIC VIOLATION
@router.get("/{violation_id}/explain")
def explain_violation_ai(
    violation_id: int,
    db: Session = Depends(get_db)
):
    violation = db.query(Violation).filter(Violation.id == violation_id).first()

    if not violation:
        return {"error": "Violation not found"}

    pilot = db.query(Pilot).filter(Pilot.id == violation.pilot_id).first()
    pilot_name = pilot.name if pilot else "Unknown Pilot"

    explanation = explain_violation(
        violation.violation_type,
        violation.description,
        pilot_name
    )

    return {
        "violation_id": violation_id,
        "pilot": pilot_name,
        "violation_type": violation.violation_type,
        "ai_explanation": explanation
    }