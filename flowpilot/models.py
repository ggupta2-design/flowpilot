from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from uuid import uuid4


@dataclass(slots=True)
class Task:
    title: str
    priority: str = "medium"
    due_date: str | None = None
    tags: list[str] = field(default_factory=list)
    id: str = ""
    completed: bool = False
    created_at: str = ""

    def __post_init__(self) -> None:
        self.title = self.title.strip()
        if not self.title:
            raise ValueError("Task title cannot be empty")
        if self.priority not in {"low", "medium", "high"}:
            raise ValueError("Priority must be low, medium, or high")
        if self.due_date:
            date.fromisoformat(self.due_date)
        self.tags = sorted({
            tag.strip().lower()
            for tag in self.tags
            if tag and tag.strip()
        })
        if not self.id:
            self.id = uuid4().hex[:8]
        if not self.created_at:
            self.created_at = datetime.now().astimezone().isoformat(timespec="seconds")

    @property
    def overdue(self) -> bool:
        return bool(
            self.due_date
            and not self.completed
            and date.fromisoformat(self.due_date) < date.today()
        )

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict) -> "Task":
        return cls(**value)
