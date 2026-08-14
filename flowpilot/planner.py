from datetime import date

from .models import Task


PRIORITY_SCORE = {"high": 0, "medium": 1, "low": 2}


def _plan_key(task: Task) -> tuple:
    due = date.fromisoformat(task.due_date) if task.due_date else date.max
    return (due, PRIORITY_SCORE[task.priority], task.created_at, task.id)


def build_daily_plan(
    tasks: list[Task],
    capacity_minutes: int,
    *,
    plan_date: date | None = None,
) -> list[Task]:
    if capacity_minutes <= 0:
        raise ValueError("Capacity must be positive")
    target = plan_date or date.today()
    candidates = [
        task
        for task in tasks
        if not task.completed and not task.archived
    ]
    candidates.sort(key=_plan_key)

    plan: list[Task] = []
    remaining = capacity_minutes
    for task in candidates:
        is_urgent = task.due_date is not None and date.fromisoformat(task.due_date) <= target
        if task.estimated_minutes <= remaining:
            plan.append(task)
            remaining -= task.estimated_minutes
        elif is_urgent and not plan:
            plan.append(task)
            break
    return plan


def planned_minutes(tasks: list[Task]) -> int:
    return sum(task.estimated_minutes for task in tasks)
