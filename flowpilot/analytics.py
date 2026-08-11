from .models import Task


def completion_stats(tasks: list[Task]) -> dict[str, int]:
    completed = sum(task.completed for task in tasks)
    total = len(tasks)
    return {
        "total": total,
        "open": total - completed,
        "done": completed,
        "rate": round((completed / total) * 100) if total else 0,
        "overdue": sum(task.overdue for task in tasks),
    }
