import csv
from pathlib import Path

from .models import Task


FIELDS = [
    "id",
    "title",
    "priority",
    "due_date",
    "tags",
    "completed",
    "archived",
    "created_at",
    "completed_at",
    "updated_at",
]


def _serialize(task: Task) -> dict[str, str | bool | None]:
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


def _truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes"}


def import_tasks(path: Path) -> list[Task]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = {"title"} - set(reader.fieldnames or [])
        if missing:
            raise ValueError("CSV must include a title column")

        tasks: list[Task] = []
        for row in reader:
            tasks.append(
                Task(
                    id=row.get("id", "").strip(),
                    title=row["title"],
                    priority=row.get("priority", "").strip() or "medium",
                    due_date=row.get("due_date", "").strip() or None,
                    tags=row.get("tags", "").split(","),
                    completed=_truthy(row.get("completed")),
                    archived=_truthy(row.get("archived")),
                    created_at=row.get("created_at", "").strip(),
                    completed_at=row.get("completed_at", "").strip() or None,
                    updated_at=row.get("updated_at", "").strip(),
                )
            )
    return tasks
