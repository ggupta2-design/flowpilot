import json

from .models import Task


def format_task(task: Task) -> str:
    marker = "x" if task.completed else " "
    alert = " OVERDUE" if task.overdue else ""
    due = f" due:{task.due_date}" if task.due_date else ""
    tags = f" tags:{','.join(task.tags)}" if task.tags else ""
    return f"[{marker}] {task.id}  {task.priority.upper():6}  {task.title}{due}{tags}{alert}"


def format_json(tasks: list[Task]) -> str:
    return json.dumps([task.to_dict() for task in tasks], indent=2)
