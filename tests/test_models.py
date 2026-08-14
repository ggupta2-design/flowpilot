from datetime import date, timedelta

import pytest

from flowpilot.models import Task


def test_task_normalizes_title_and_generates_id() -> None:
    task = Task("  Send weekly report  ")
    assert task.title == "Send weekly report"
    assert len(task.id) == 8


def test_task_rejects_invalid_priority() -> None:
    with pytest.raises(ValueError, match="Priority"):
        Task("Run backup", priority="urgent")


def test_overdue_excludes_completed_tasks() -> None:
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    assert Task("Run backup", due_date=yesterday).overdue
    assert not Task("Run backup", due_date=yesterday, completed=True).overdue


def test_task_requires_positive_effort_estimate() -> None:
    with pytest.raises(ValueError):
        Task("Impossible estimate", estimated_minutes=0)


def test_task_requires_timezone_aware_reminder() -> None:
    with pytest.raises(ValueError):
        Task("Ambiguous reminder", remind_at="2030-01-01T09:00:00")


def test_task_accepts_timezone_aware_reminder() -> None:
    task = Task("Clear reminder", remind_at="2030-01-01T09:00:00-05:00")
    assert task.remind_at == "2030-01-01T09:00:00-05:00"
