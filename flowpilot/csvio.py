import csv
from pathlib import Path

from .models import Task


FIELDS = ["id", "title", "priority", "due_date", "completed", "created_at"]


def export_tasks(tasks: list[Task], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(task.to_dict() for task in tasks)
    return len(tasks)
