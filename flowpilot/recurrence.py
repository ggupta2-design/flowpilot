from datetime import date, timedelta


FREQUENCIES = {"daily", "weekly", "monthly"}


def next_due_date(current_due_date: str, frequency: str) -> str:
    if frequency not in FREQUENCIES:
        raise ValueError("Frequency must be daily, weekly, or monthly")

    current = date.fromisoformat(current_due_date)
    if frequency == "daily":
        return (current + timedelta(days=1)).isoformat()
    if frequency == "weekly":
        return (current + timedelta(days=7)).isoformat()

    year = current.year + (1 if current.month == 12 else 0)
    month = 1 if current.month == 12 else current.month + 1
    first_after_target = date(year + (1 if month == 12 else 0), 1 if month == 12 else month + 1, 1)
    last_day = (first_after_target - timedelta(days=1)).day
    return date(year, month, min(current.day, last_day)).isoformat()
