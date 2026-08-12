from flowpilot.models import Task
from flowpilot.sorting import sort_tasks


def test_sort_by_priority_then_due_date() -> None:
    tasks = [
        Task("Low", priority="low", due_date="2030-01-01"),
        Task("High later", priority="high", due_date="2030-02-01"),
        Task("High sooner", priority="high", due_date="2030-01-01"),
    ]
    assert [task.title for task in sort_tasks(tasks, "priority")] == [
        "High sooner",
        "High later",
        "Low",
    ]


def test_undated_tasks_sort_last_by_due_date() -> None:
    tasks = [Task("Undated"), Task("Dated", due_date="2030-01-01")]
    assert [task.title for task in sort_tasks(tasks, "due")] == ["Dated", "Undated"]
