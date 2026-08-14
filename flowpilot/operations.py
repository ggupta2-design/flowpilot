from datetime import datetime

from .models import Task


def complete_task(task: Task) -> None:
    if not task.completed:
        task.completed = True
        task.completed_at = datetime.now().astimezone().isoformat(timespec="seconds")
        task.touch()


def reopen_task(task: Task) -> None:
    if task.completed:
        task.completed = False
        task.completed_at = None
        task.touch()


def archive_task(task: Task) -> None:
    if not task.archived:
        task.archived = True
        task.touch()


def restore_task(task: Task) -> None:
    if task.archived:
        task.archived = False
        task.touch()


def edit_task(
    task: Task,
    *,
    title: str | None = None,
    priority: str | None = None,
    due_date: str | None = None,
    clear_due_date: bool = False,
    tags: list[str] | None = None,
    estimated_minutes: int | None = None,
    remind_at: str | None = None,
    clear_reminder: bool = False,
) -> None:
    candidate = Task(
        id=task.id,
        title=title if title is not None else task.title,
        priority=priority if priority is not None else task.priority,
        due_date=None if clear_due_date else (due_date if due_date is not None else task.due_date),
        tags=tags if tags is not None else task.tags,
        estimated_minutes=estimated_minutes if estimated_minutes is not None else task.estimated_minutes,
        remind_at=None if clear_reminder else (remind_at if remind_at is not None else task.remind_at),
        completed=task.completed,
        archived=task.archived,
        created_at=task.created_at,
        completed_at=task.completed_at,
        updated_at=task.updated_at,
    )
    task.title = candidate.title
    task.priority = candidate.priority
    task.due_date = candidate.due_date
    task.tags = candidate.tags
    task.estimated_minutes = candidate.estimated_minutes
    task.remind_at = candidate.remind_at
    task.touch()
