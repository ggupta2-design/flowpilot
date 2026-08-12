from flowpilot.filtering import filter_tasks
from flowpilot.models import Task


def test_tags_are_normalized_and_deduplicated() -> None:
    task = Task("Report", tags=[" Work ", "work", "", "Weekly"])
    assert task.tags == ["weekly", "work"]


def test_filter_by_tag() -> None:
    tasks = [
        Task("Report", tags=["work"]),
        Task("Groceries", tags=["home"]),
    ]
    assert [task.title for task in filter_tasks(tasks, tag="WORK")] == ["Report"]


def test_filter_by_priority_and_tag() -> None:
    tasks = [
        Task("Urgent report", priority="high", tags=["work"]),
        Task("Routine report", priority="low", tags=["work"]),
    ]
    result = filter_tasks(tasks, priority="high", tag="work")
    assert [task.title for task in result] == ["Urgent report"]
