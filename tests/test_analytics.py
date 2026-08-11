from datetime import date, timedelta

from flowpilot.analytics import completion_stats
from flowpilot.models import Task


def test_completion_stats() -> None:
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    tasks = [
        Task("Done", completed=True),
        Task("Late", due_date=yesterday),
        Task("Open"),
    ]
    assert completion_stats(tasks) == {
        "total": 3,
        "open": 2,
        "done": 1,
        "rate": 33,
        "overdue": 1,
    }


def test_empty_stats() -> None:
    assert completion_stats([])["rate"] == 0
