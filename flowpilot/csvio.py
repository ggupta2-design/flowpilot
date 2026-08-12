import csv
from pathlib import Path

from .models import Task


FIELDS = ["id", "title", "priority", "due_date", "tags", "completed", "created_at"]


def _serialize(task: Task) -> dict[str, str | bool]:
    value = task.to_dict()
    value["tags"] = ",".join(task.tags)
    return value


def export_tasks(tasks: list[Task], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(_serialize(task) for task in tasks)
    return len(tasks)


def import_tasks(path: Path) -> list[Task]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = {"title"} - set(reader.fieldnames or [])
        if missing:
            raise ValueError("CSV must include a title column")

        tasks: list[Task] = []
        for row in reader:
            completed = row.get("completed", "").strip().lower() in {"1", "true", "yes"}
            tasks.append(
                Task(
                    id=row.get("id", "").strip(),
                    title=row["title"],
                    priority=row.get("priority", "").strip() or "medium",
                    due_date=row.get("due_date", "").strip() or None,
                    tags=row.get("tags", "").split(","),
                    completed=completed,
                    created_at=row.get("created_at", "").strip(),
                )
            )
    return tasks
