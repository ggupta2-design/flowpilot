import csv
from pathlib import Path

from flowpilot.csvio import export_tasks, import_tasks
from flowpilot.models import Task


def test_csv_export(tmp_path: Path) -> None:
    destination = tmp_path / "exports" / "tasks.csv"
    count = export_tasks([Task("Send report", priority="high")], destination)
    rows = list(csv.DictReader(destination.open(encoding="utf-8")))
    assert count == 1
    assert rows[0]["title"] == "Send report"
    assert rows[0]["priority"] == "high"


def test_csv_round_trip_preserves_planning_metadata(tmp_path: Path) -> None:
    destination = tmp_path / "tasks.csv"
    task = Task(
        "Follow up",
        estimated_minutes=45,
        remind_at="2030-01-01T09:00:00-05:00",
        snoozed_until="2030-01-01T10:30:00-05:00",
        tags=["client"],
    )

    export_tasks([task], destination)
    restored = import_tasks(destination)

    assert restored[0].to_dict() == task.to_dict()


def test_csv_import_remains_compatible_without_new_columns(tmp_path: Path) -> None:
    destination = tmp_path / "legacy.csv"
    destination.write_text("title,priority\nLegacy task,high\n", encoding="utf-8")

    restored = import_tasks(destination)

    assert restored[0].title == "Legacy task"
    assert restored[0].snoozed_until is None
