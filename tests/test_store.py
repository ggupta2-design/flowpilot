from pathlib import Path

from flowpilot.models import Task
from flowpilot.store import TaskStore


def test_store_round_trip(tmp_path: Path) -> None:
    store = TaskStore(tmp_path / "tasks.json")
    original = Task("Publish report", priority="high", due_date="2030-01-01")
    store.save([original])
    assert store.load() == [original]


def test_missing_store_is_empty(tmp_path: Path) -> None:
    assert TaskStore(tmp_path / "missing.json").load() == []
