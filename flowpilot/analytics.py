from datetime import datetime

from .models import Task
from .reminders import reminders_ready


def completion_stats(
    tasks: list[Task],
    *,
    now: datetime | None = None,
) -> dict[str, int]:
    active = [task for task in tasks if not task.archived]
    completed = sum(task.completed for task in active)
    open_tasks = [task for task in active if not task.completed]
    total = len(active)
    return {
        "total": total,
        "open": len(open_tasks),
        "done": completed,
        "rate": round((completed / total) * 100) if total else 0,
        "overdue": sum(task.overdue for task in active),
        "archived": sum(task.archived for task in tasks),
        "remaining_minutes": sum(task.estimated_minutes for task in open_tasks),
        "scheduled_reminders": sum(bool(task.remind_at) for task in open_tasks),
        "ready_reminders": len(reminders_ready(tasks, now=now)),
    }
