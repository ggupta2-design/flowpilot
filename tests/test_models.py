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
