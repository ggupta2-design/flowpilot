from flowpilot.filtering import filter_tasks
from flowpilot.models import Task


def test_filter_by_status() -> None:
    tasks = [Task("Open"), Task("Done", completed=True)]
    assert [task.title for task in filter_tasks(tasks, status="open")] == ["Open"]
    assert [task.title for task in filter_tasks(tasks, status="done")] == ["Done"]


def test_search_is_case_insensitive() -> None:
    tasks = [Task("Send Weekly Report"), Task("Run backup")]
    result = filter_tasks(tasks, search="weekly")
    assert [task.title for task in result] == ["Send Weekly Report"]
