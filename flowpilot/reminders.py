from datetime import datetime

from .models import Task


def reminders_ready(
    tasks: list[Task],
    *,
    now: datetime | None = None,
) -> list[Task]:
    current = now or datetime.now().astimezone()
    if current.utcoffset() is None:
        raise ValueError("Current time must include a timezone")

    ready = [
        task
        for task in tasks
        if task.remind_at
        and not task.completed
        and not task.archived
        and datetime.fromisoformat(task.remind_at) <= current
    ]
    return sorted(
        ready,
        key=lambda task: (task.remind_at or "", task.due_date or "9999-12-31", task.id),
    )
