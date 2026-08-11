import csv
from pathlib import Path

from flowpilot.csvio import export_tasks
from flowpilot.models import Task


def test_csv_export(tmp_path: Path) -> None:
    destination = tmp_path / "exports" / "tasks.csv"
    count = export_tasks([Task("Send report", priority="high")], destination)
    rows = list(csv.DictReader(destination.open(encoding="utf-8")))
    assert count == 1
    assert rows[0]["title"] == "Send report"
    assert rows[0]["priority"] == "high"
