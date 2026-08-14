from flowpilot.models import Task
from flowpilot.operations import archive_task, complete_task, edit_task, reopen_task, restore_task


def test_complete_and_reopen_are_reversible() -> None:
    task = Task("Ship report")
    complete_task(task)
    assert task.completed
    assert task.completed_at is not None
    reopen_task(task)
    assert not task.completed
    assert task.completed_at is None


def test_archive_and_restore_are_reversible() -> None:
    task = Task("Old task")
    archive_task(task)
    assert task.archived
    restore_task(task)
    assert not task.archived


def test_edit_validates_and_normalizes_fields() -> None:
    task = Task("Draft", tags=["old"])
    edit_task(
        task,
        title=" Final report ",
        priority="high",
        due_date="2030-02-01",
        tags=["Work", "work"],
    )
    assert task.title == "Final report"
    assert task.priority == "high"
    assert task.due_date == "2030-02-01"
    assert task.tags == ["work"]


def test_edit_can_clear_due_date() -> None:
    task = Task("Report", due_date="2030-02-01")
    edit_task(task, clear_due_date=True)
    assert task.due_date is None


def test_edit_updates_planning_metadata() -> None:
    task = Task("Report")
    edit_task(
        task,
        estimated_minutes=75,
        remind_at="2030-02-01T09:00:00-05:00",
    )
    assert task.estimated_minutes == 75
    assert task.remind_at == "2030-02-01T09:00:00-05:00"


def test_edit_can_clear_reminder() -> None:
    task = Task("Report", remind_at="2030-02-01T09:00:00-05:00")
    edit_task(task, clear_reminder=True)
    assert task.remind_at is None
