from pathlib import Path

import pytest

from flowpilot.models import Task
from flowpilot.store import TaskStore


def test_store_round_trip(tmp_path: Path) -> None:
    store = TaskStore(tmp_path / "tasks.json")
    original = Task("Publish report", priority="high", due_date="2030-01-01")
    store.save([original])
    assert store.load() == [original]


def test_missing_store_is_empty(tmp_path: Path) -> None:
    assert TaskStore(tmp_path / "missing.json").load() == []


def test_second_save_preserves_previous_snapshot(tmp_path: Path) -> None:
    store = TaskStore(tmp_path / "tasks.json")
    first = Task("First")
    store.save([first])
    store.save([Task("Second")])
    assert store.recovery_path.exists()
    assert store.recover() == [first]


def test_recover_requires_snapshot(tmp_path: Path) -> None:
    store = TaskStore(tmp_path / "tasks.json")
    with pytest.raises(FileNotFoundError, match="recovery"):
        store.recover()
