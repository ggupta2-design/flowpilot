import json
from pathlib import Path

from .models import Task


class TaskStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path.home() / ".flowpilot" / "tasks.json"

    def load(self) -> list[Task]:
        if not self.path.exists():
            return []
        try:
            content = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError(f"Task store contains invalid JSON: {self.path}") from error
        if not isinstance(content, list):
            raise ValueError(f"Task store must contain a JSON list: {self.path}")
        try:
            return [Task.from_dict(item) for item in content]
        except (TypeError, ValueError) as error:
            raise ValueError(f"Task store contains an invalid task: {self.path}") from error

    def save(self, tasks: list[Task]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps([task.to_dict() for task in tasks], indent=2),
            encoding="utf-8",
        )
        temporary.replace(self.path)
