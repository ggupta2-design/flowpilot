import json
from datetime import datetime
from pathlib import Path

from .models import Task


BACKUP_VERSION = 1


def create_backup(tasks: list[Task], destination: Path) -> int:
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": BACKUP_VERSION,
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "tasks": [task.to_dict() for task in tasks],
    }
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    temporary.replace(destination)
    return len(tasks)


def read_backup(source: Path) -> list[Task]:
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Backup contains invalid JSON: {source}") from error
    if not isinstance(payload, dict) or payload.get("version") != BACKUP_VERSION:
        raise ValueError("Unsupported or missing backup version")
    records = payload.get("tasks")
    if not isinstance(records, list):
        raise ValueError("Backup must contain a task list")
    try:
        return [Task.from_dict(record) for record in records]
    except (TypeError, ValueError) as error:
        raise ValueError("Backup contains an invalid task") from error


def merge_backup(current: list[Task], incoming: list[Task]) -> list[Task]:
    current_ids = {task.id for task in current}
    duplicates = current_ids.intersection(task.id for task in incoming)
    if duplicates:
        ids = ", ".join(sorted(duplicates))
        raise ValueError(f"Backup contains existing task IDs: {ids}")
    return [*current, *incoming]
