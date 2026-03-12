from sqlalchemy.orm import Session
from datetime import timedelta

from backend.app.utils.time_utils import calculate_hours
from backend.app.services.violation_service import create_violation

MAX_DUTY_HOURS = 13
MIN_REST_HOURS = 10
MAX_FLIGHT_HOURS_DAY = 8


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


def check_rest_period(
    db: Session,
    pilot_id: int,
    rest_start,
    rest_end
):

    rest_hours = calculate_hours(rest_start, rest_end)

    if rest_hours < MIN_REST_HOURS:

        create_violation(
            db,
            pilot_id,
            "REST_INSUFFICIENT",
            f"Rest below {MIN_REST_HOURS} hours. Actual: {rest_hours}",
            "HIGH"
        )