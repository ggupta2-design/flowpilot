from pathlib import Path

import pytest

from flowpilot.csvio import export_tasks, import_tasks
from flowpilot.models import Task


def test_csv_round_trip_preserves_tags(tmp_path: Path) -> None:
    path = tmp_path / "tasks.csv"
    original = Task("Report", priority="high", tags=["Work", "weekly"], completed=True)
    export_tasks([original], path)
    assert import_tasks(path) == [original]


def test_import_requires_title_column(tmp_path: Path) -> None:
    path = tmp_path / "invalid.csv"
    path.write_text("priority,due_date\nhigh,2030-01-01\n", encoding="utf-8")
    with pytest.raises(ValueError, match="title"):
        import_tasks(path)
