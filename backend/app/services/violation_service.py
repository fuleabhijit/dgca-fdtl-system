from sqlalchemy.orm import Session
from app.models.violation import Violation

def create_violation(
    db: Session,
    pilot_id: int,
    violation_type: str,
    description: str,
    severity: str = "MEDIUM"
):

    violation = Violation(
        pilot_id=pilot_id,
        violation_type=violation_type,
        description=description,
        severity=severity
    )

    db.add(violation)
    db.commit()

    return violation