from datetime import datetime, timezone

import pytest

from flowpilot.models import Task
from flowpilot.reminders import reminders_ready


NOW = datetime(2030, 1, 1, 12, 0, tzinfo=timezone.utc)


def test_ready_reminders_are_sorted_and_filtered() -> None:
    tasks = [
        Task("Later", remind_at="2030-01-01T13:00:00+00:00"),
        Task("Ready second", remind_at="2030-01-01T11:30:00+00:00"),
        Task("Ready first", remind_at="2030-01-01T10:00:00+00:00"),
        Task("Done", completed=True, remind_at="2030-01-01T09:00:00+00:00"),
        Task("Archived", archived=True, remind_at="2030-01-01T08:00:00+00:00"),
        Task("Unscheduled"),
    ]

    ready = reminders_ready(tasks, now=NOW)

    assert [task.title for task in ready] == ["Ready first", "Ready second"]


def test_reminder_comparison_requires_timezone_aware_now() -> None:
    with pytest.raises(ValueError, match="timezone"):
        reminders_ready([], now=datetime(2030, 1, 1, 12, 0))
