import json
from pathlib import Path

from .models import Task


class TaskStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path.home() / ".flowpilot" / "tasks.json"

    def load(self) -> list[Task]:
        if not self.path.exists():
            return []
        content = json.loads(self.path.read_text(encoding="utf-8"))
        return [Task.from_dict(item) for item in content]

    def save(self, tasks: list[Task]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps([task.to_dict() for task in tasks], indent=2),
            encoding="utf-8",
        )
        temporary.replace(self.path)
