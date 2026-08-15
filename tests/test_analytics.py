from datetime import date, datetime, timedelta, timezone

from flowpilot.analytics import completion_stats
from flowpilot.models import Task


NOW = datetime(2030, 1, 1, 12, 0, tzinfo=timezone.utc)


def test_completion_stats() -> None:
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    tasks = [
        Task("Done", completed=True, estimated_minutes=15),
        Task(
            "Late",
            due_date=yesterday,
            estimated_minutes=45,
            remind_at="2030-01-01T11:00:00+00:00",
        ),
        Task(
            "Open",
            estimated_minutes=30,
            remind_at="2030-01-01T11:00:00+00:00",
            snoozed_until="2030-01-01T14:00:00+00:00",
        ),
        Task("Archived", archived=True, due_date=yesterday, estimated_minutes=90),
    ]
    assert completion_stats(tasks, now=NOW) == {
        "total": 3,
        "open": 2,
        "done": 1,
        "rate": 33,
        "overdue": 1,
        "archived": 1,
        "remaining_minutes": 75,
        "scheduled_reminders": 2,
        "ready_reminders": 1,
    }


def test_empty_stats() -> None:
    assert completion_stats([], now=NOW) == {
        "total": 0,
        "open": 0,
        "done": 0,
        "rate": 0,
        "overdue": 0,
        "archived": 0,
        "remaining_minutes": 0,
        "scheduled_reminders": 0,
        "ready_reminders": 0,
    }
