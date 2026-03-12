from datetime import datetime


def calculate_hours(start: datetime, end: datetime):

    diff = end - start

    hours = diff.total_seconds() / 3600

    return hours