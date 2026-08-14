from datetime import date, timedelta

from flowpilot.analytics import completion_stats
from flowpilot.models import Task


def test_completion_stats() -> None:
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    tasks = [
        Task("Done", completed=True, estimated_minutes=15),
        Task("Late", due_date=yesterday, estimated_minutes=45),
        Task("Open", estimated_minutes=30),
        Task("Archived", archived=True, due_date=yesterday, estimated_minutes=90),
    ]
    assert completion_stats(tasks) == {
        "total": 3,
        "open": 2,
        "done": 1,
        "rate": 33,
        "overdue": 1,
        "archived": 1,
        "remaining_minutes": 75,
    }


def test_empty_stats() -> None:
    assert completion_stats([]) == {
        "total": 0,
        "open": 0,
        "done": 0,
        "rate": 0,
        "overdue": 0,
        "archived": 0,
        "remaining_minutes": 0,
    }
