from datetime import date

import pytest

from flowpilot.models import Task
from flowpilot.planner import build_daily_plan, planned_minutes


def test_plan_respects_capacity_and_due_date_order() -> None:
    tasks = [
        Task("Later high priority", priority="high", due_date="2030-01-02", estimated_minutes=60),
        Task("Due today", priority="medium", due_date="2030-01-01", estimated_minutes=30),
        Task("Undated", estimated_minutes=30),
    ]

    plan = build_daily_plan(tasks, 90, plan_date=date(2030, 1, 1))

    assert [task.title for task in plan] == ["Due today", "Later high priority"]
    assert planned_minutes(plan) == 90


def test_plan_excludes_completed_and_archived_tasks() -> None:
    tasks = [
        Task("Open", estimated_minutes=20),
        Task("Done", completed=True, estimated_minutes=10),
        Task("Archived", archived=True, estimated_minutes=10),
    ]

    assert [task.title for task in build_daily_plan(tasks, 60)] == ["Open"]


def test_urgent_task_can_exceed_capacity_when_plan_is_empty() -> None:
    urgent = Task("Handle outage", due_date="2030-01-01", estimated_minutes=90)

    assert build_daily_plan([urgent], 30, plan_date=date(2030, 1, 1)) == [urgent]


def test_plan_requires_positive_capacity() -> None:
    with pytest.raises(ValueError, match="positive"):
        build_daily_plan([], 0)
