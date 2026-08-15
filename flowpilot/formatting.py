import json

from .models import Task
from .reminders import reminder_time


def format_task(task: Task) -> str:
    marker = "x" if task.completed else " "
    alert = " OVERDUE" if task.overdue else ""
    archived = " ARCHIVED" if task.archived else ""
    due = f" due:{task.due_date}" if task.due_date else ""
    tags = f" tags:{','.join(task.tags)}" if task.tags else ""
    reminder = f" remind:{task.remind_at}" if task.remind_at else ""
    snooze = f" snoozed-until:{task.snoozed_until}" if task.snoozed_until else ""
    effective = reminder_time(task)
    ready_at = (
        f" next-alert:{effective.isoformat(timespec='seconds')}"
        if effective and task.snoozed_until
        else ""
    )
    effort = f" estimate:{task.estimated_minutes}m"
    return (
        f"[{marker}] {task.id}  {task.priority.upper():6}  {task.title}"
        f"{due}{tags}{effort}{reminder}{snooze}{ready_at}{alert}{archived}"
    )


def format_json(tasks: list[Task]) -> str:
    return json.dumps([task.to_dict() for task in tasks], indent=2)
