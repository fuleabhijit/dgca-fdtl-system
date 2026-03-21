from sqlalchemy.orm import Session
from app.models.violation import Violation
import requests

N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/f2482a4b-de52-4284-9a92-7ded7ee4b607"


def create_violation(db: Session, pilot_id: int, violation_type: str, description: str, severity: str):

    violation = Violation(
        pilot_id=pilot_id,
        violation_type=violation_type,
        description=description,
        severity=severity
    )

    db.add(violation)
    db.commit()

    # Fire n8n webhook for HIGH violations
    if severity == "HIGH":
        try:
            requests.post(
                N8N_WEBHOOK_URL,
                json={
                    "pilot_id":       pilot_id,
                    "violation_type": violation_type,
                    "description":    description,
                    "severity":       severity
                },
                timeout=3
            )
            print(f"[n8n] Webhook fired for HIGH violation — pilot {pilot_id}")
        except Exception as e:
            print(f"[n8n] Webhook failed: {e}")

    return violation