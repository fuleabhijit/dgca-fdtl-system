from sqlalchemy.orm import Session
from datetime import timedelta
from app.utils.time_utils import calculate_hours
from app.services.violation_service import create_violation
from app.models.duty_period import DutyPeriod

# DGCA FDTL Limits
MAX_DUTY_HOURS = 13          # Max single duty period
MAX_FLIGHT_DUTY_HOURS = 10   # Max flight duty (subset of total duty)
MIN_REST_HOURS = 10          # Minimum rest between duties
MAX_WEEKLY_HOURS = 60        # Max duty in any 7-day window

def check_duty_period(db: Session, pilot_id: int, duty_start, duty_end):
    duty_hours = calculate_hours(duty_start, duty_end)
    violations = []

    # Rule 1: Single duty period limit
    if duty_hours > MAX_DUTY_HOURS:
        violations.append(create_violation(
            db, pilot_id,
            "DUTY_LIMIT_EXCEEDED",
            f"Duty period of {duty_hours:.1f}h exceeds DGCA max of {MAX_DUTY_HOURS}h",
            "HIGH"
        ))

    # Rule 2: Minimum rest between duties
    previous_duty = (
        db.query(DutyPeriod)
        .filter(DutyPeriod.pilot_id == pilot_id)
        .filter(DutyPeriod.duty_end < duty_start)
        .order_by(DutyPeriod.duty_end.desc())
        .first()
    )

    if previous_duty:
        rest_hours = calculate_hours(previous_duty.duty_end, duty_start)
        if rest_hours < MIN_REST_HOURS:
            violations.append(create_violation(
                db, pilot_id,
                "INSUFFICIENT_REST",
                f"Rest period of {rest_hours:.1f}h is below DGCA minimum of {MIN_REST_HOURS}h",
                "HIGH"
            ))

    # Rule 3: 7-day rolling window
    window_start = duty_start - timedelta(days=7)
    recent_duties = (
        db.query(DutyPeriod)
        .filter(DutyPeriod.pilot_id == pilot_id)
        .filter(DutyPeriod.duty_start >= window_start)
        .all()
    )

    total_weekly = sum(d.duration_hours or 0 for d in recent_duties) + duty_hours
    if total_weekly > MAX_WEEKLY_HOURS:
        violations.append(create_violation(
            db, pilot_id,
            "WEEKLY_LIMIT_EXCEEDED",
            f"7-day total duty of {total_weekly:.1f}h exceeds DGCA max of {MAX_WEEKLY_HOURS}h",
            "MEDIUM"
        ))

    return violations