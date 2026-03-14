from sqlalchemy.orm import Session
from app.utils.time_utils import calculate_hours
from app.services.violation_service import create_violation

MAX_DUTY_HOURS = 13
MIN_REST_HOURS = 10


def check_duty_period(
    db: Session,
    pilot_id: int,
    duty_start,
    duty_end
):

    duty_hours = calculate_hours(duty_start, duty_end)

    if duty_hours > MAX_DUTY_HOURS:

        create_violation(
            db,
            pilot_id,
            "DUTY_LIMIT_EXCEEDED",
            f"Duty exceeded {MAX_DUTY_HOURS} hours. Actual: {duty_hours}",
            "HIGH"
        )