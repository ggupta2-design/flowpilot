from datetime import datetime

from .models import Task


def _aware(value: datetime, *, label: str) -> datetime:
    if value.utcoffset() is None:
        raise ValueError(f"{label} must include a timezone")
    return value


def reminder_time(task: Task) -> datetime | None:
    """Return the effective delivery time after any snooze."""
    if not task.remind_at:
        return None
    scheduled = datetime.fromisoformat(task.remind_at)
    if not task.snoozed_until:
        return scheduled
    return max(scheduled, datetime.fromisoformat(task.snoozed_until))


def reminders_ready(
    tasks: list[Task],
    *,
    now: datetime | None = None,
) -> list[Task]:
    current = _aware(now or datetime.now().astimezone(), label="Current time")
    ready = [
        task
        for task in tasks
        if reminder_time(task) is not None
        and not task.completed
        and not task.archived
        and reminder_time(task) <= current
    ]
    return sorted(
        ready,
        key=lambda task: (reminder_time(task), task.due_date or "9999-12-31", task.id),
    )


def snooze_task(
    task: Task,
    until: str,
    *,
    now: datetime | None = None,
) -> None:
    if not task.remind_at:
        raise ValueError("Cannot snooze a task without a reminder")
    if task.completed or task.archived:
        raise ValueError("Cannot snooze an inactive task")
    current = _aware(now or datetime.now().astimezone(), label="Current time")
    snooze_until = _aware(datetime.fromisoformat(until), label="Snooze timestamp")
    if snooze_until <= current:
        raise ValueError("Snooze timestamp must be in the future")
    task.snoozed_until = until
    task.touch()


def clear_snooze(task: Task) -> None:
    if task.snoozed_until is not None:
        task.snoozed_until = None
        task.touch()
