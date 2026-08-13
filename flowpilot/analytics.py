from .models import Task


def completion_stats(tasks: list[Task]) -> dict[str, int]:
    active = [task for task in tasks if not task.archived]
    completed = sum(task.completed for task in active)
    total = len(active)
    return {
        "total": total,
        "open": total - completed,
        "done": completed,
        "rate": round((completed / total) * 100) if total else 0,
        "overdue": sum(task.overdue for task in active),
        "archived": sum(task.archived for task in tasks),
    }
