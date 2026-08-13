import json
from pathlib import Path

import pytest

from flowpilot.backup import create_backup, merge_backup, read_backup
from flowpilot.models import Task


def test_backup_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "backup.json"
    original = Task("Report", tags=["work"], archived=True)
    assert create_backup([original], path) == 1
    assert read_backup(path) == [original]


def test_backup_rejects_unknown_version(tmp_path: Path) -> None:
    path = tmp_path / "backup.json"
    path.write_text(json.dumps({"version": 99, "tasks": []}), encoding="utf-8")
    with pytest.raises(ValueError, match="version"):
        read_backup(path)


def test_merge_rejects_duplicate_ids() -> None:
    task = Task("Report")
    with pytest.raises(ValueError, match=task.id):
        merge_backup([task], [task])
