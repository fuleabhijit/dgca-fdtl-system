from datetime import datetime

from app.database import SessionLocal
from app.services.rule_engine import check_duty_period


db = SessionLocal()

check_duty_period(
    db,
    pilot_id=1,
    duty_start=datetime(2025, 1, 1, 6, 0),
    duty_end=datetime(2025, 1, 1, 22, 0)
)

print("Rule engine test executed")