from datetime import datetime, timezone

import pytest

from flowpilot.models import Task
from flowpilot.reminders import clear_snooze, reminder_time, reminders_ready, snooze_task


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


def test_snooze_defers_a_ready_reminder() -> None:
    task = Task("Follow up", remind_at="2030-01-01T11:00:00+00:00")

    snooze_task(task, "2030-01-01T14:00:00+00:00", now=NOW)

    assert reminder_time(task) == datetime(2030, 1, 1, 14, 0, tzinfo=timezone.utc)
    assert reminders_ready([task], now=NOW) == []


def test_clear_snooze_restores_original_schedule() -> None:
    task = Task(
        "Follow up",
        remind_at="2030-01-01T11:00:00+00:00",
        snoozed_until="2030-01-01T14:00:00+00:00",
    )

    clear_snooze(task)

    assert task.snoozed_until is None
    assert reminders_ready([task], now=NOW) == [task]


@pytest.mark.parametrize(
    "task",
    [
        Task("Missing reminder"),
        Task("Completed", completed=True, remind_at="2030-01-01T11:00:00+00:00"),
        Task("Archived", archived=True, remind_at="2030-01-01T11:00:00+00:00"),
    ],
)
def test_snooze_rejects_ineligible_tasks(task: Task) -> None:
    with pytest.raises(ValueError):
        snooze_task(task, "2030-01-01T14:00:00+00:00", now=NOW)


def test_snooze_requires_a_future_aware_timestamp() -> None:
    task = Task("Follow up", remind_at="2030-01-01T11:00:00+00:00")
    with pytest.raises(ValueError):
        snooze_task(task, "2030-01-01T12:00:00+00:00", now=NOW)
    with pytest.raises(ValueError, match="timezone"):
        snooze_task(task, "2030-01-01T14:00:00", now=NOW)
