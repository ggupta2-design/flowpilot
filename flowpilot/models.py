from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from uuid import uuid4


def _timestamp() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _validate_aware_timestamp(value: str, *, field_name: str) -> None:
    parsed = datetime.fromisoformat(value)
    if parsed.utcoffset() is None:
        raise ValueError(`${field_name} timestamp must include a timezone`)


@dataclass(slots=True)
class Task:
    title: str
    priority: str = "medium"
    due_date: str | None = None
    tags: list[str] = field(default_factory=list)
    estimated_minutes: int = 30
    remind_at: str | None = None
    snoozed_until: str | None = None
    id: str = ""
    completed: bool = False
    archived: bool = False
    created_at: str = ""
    completed_at: str | None = None
    updated_at: str = ""

    def __post_init__(self) -> None:
        self.title = self.title.strip()
        if not self.title:
            raise ValueError("Task title cannot be empty")
        if self.priority not in {"low", "medium", "high"}:
            raise ValueError("Priority must be low, medium, or high")
        if self.due_date:
            date.fromisoformat(self.due_date)
        if not isinstance(self.estimated_minutes, int) or self.estimated_minutes <= 0:
            raise ValueError("Estimated minutes must be a positive integer")
        if self.remind_at:
            _validate_aware_timestamp(self.remind_at, field_name="Reminder")
        if self.snoozed_until:
            _validate_aware_timestamp(self.snoozed_until, field_name="Snooze")
            if not self.remind_at:
                raise ValueError("A snooze requires a reminder")
        self.tags = sorted({
            tag.strip().lower()
            for tag in self.tags
            if tag and tag.strip()
        })
        if not self.id:
            self.id = uuid4().hex[:8]
        if not self.created_at:
            self.created_at = _timestamp()
        if not self.updated_at:
            self.updated_at = self.created_at

    @property
    def overdue(self) -> bool:
        return bool(
            self.due_date
            and not self.completed
            and not self.archived
            and date.fromisoformat(self.due_date) < date.today()
        )

    def touch(self) -> None:
        self.updated_at = _timestamp()

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict) -> "Task":
        return cls(**value)
