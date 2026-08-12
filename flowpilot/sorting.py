from datetime import date

from .models import Task


PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


def sort_tasks(tasks: list[Task], sort_by: str = "created") -> list[Task]:
    if sort_by == "created":
        return sorted(tasks, key=lambda task: (task.created_at, task.id))
    if sort_by == "priority":
        return sorted(
            tasks,
            key=lambda task: (PRIORITY_RANK[task.priority], task.due_date or "9999-12-31", task.title.casefold()),
        )
    if sort_by == "due":
        return sorted(
            tasks,
            key=lambda task: (
                date.fromisoformat(task.due_date) if task.due_date else date.max,
                PRIORITY_RANK[task.priority],
                task.title.casefold(),
            ),
        )
    raise ValueError("Sort must be created, priority, or due")
