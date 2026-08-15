import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from .models import Task


PRIORITIES = {"low", "medium", "high"}


@dataclass(frozen=True, slots=True)
class Rule:
    name: str
    match_priority: str | None = None
    match_tag: str | None = None
    title_contains: str | None = None
    set_priority: str | None = None
    add_tags: tuple[str, ...] = ()
    due_in_days: int | None = None
    remind_in_hours: int | None = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Rule name cannot be empty")
        for priority in (self.match_priority, self.set_priority):
            if priority and priority not in PRIORITIES:
                raise ValueError("Rule priority must be low, medium, or high")
        for label, value in (
            ("due_in_days", self.due_in_days),
            ("remind_in_hours", self.remind_in_hours),
        ):
            if value is not None and (not isinstance(value, int) or value < 0):
                raise ValueError(f"{label} must be a non-negative integer")

    def matches(self, task: Task) -> bool:
        if task.completed or task.archived:
            return False
        if self.match_priority and task.priority != self.match_priority:
            return False
        if self.match_tag and self.match_tag.strip().lower() not in task.tags:
            return False
        if self.title_contains and self.title_contains.casefold() not in task.title.casefold():
            return False
        return True

    @classmethod
    def from_dict(cls, value: dict) -> "Rule":
        allowed = {
            "name",
            "match_priority",
            "match_tag",
            "title_contains",
            "set_priority",
            "add_tags",
            "due_in_days",
            "remind_in_hours",
        }
        unknown = set(value) - allowed
        if unknown:
            raise ValueError(f"Unsupported rule fields: {', '.join(sorted(unknown))}")
        if "name" not in value:
            raise ValueError("Every rule requires a name")
        tags = value.get("add_tags", [])
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            raise ValueError("add_tags must be a list of strings")
        return cls(**{**value, "add_tags": tuple(tags)})


def load_rules(path: Path) -> list[Rule]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid rules JSON: {error.msg}") from error
    if not isinstance(payload, list):
        raise ValueError("Rules file must contain a JSON list")
    if not all(isinstance(item, dict) for item in payload):
        raise ValueError("Every rule must be a JSON object")
    return [Rule.from_dict(item) for item in payload]


def apply_rules(
    tasks: list[Task],
    rules: list[Rule],
    *,
    now: datetime | None = None,
) -> list[tuple[str, str]]:
    current = now or datetime.now().astimezone()
    if current.utcoffset() is None:
        raise ValueError("Current time must include a timezone")

    applied: list[tuple[str, str]] = []
    for task in tasks:
        for rule in rules:
            if not rule.matches(task):
                continue
            changed = False
            if rule.set_priority and task.priority != rule.set_priority:
                task.priority = rule.set_priority
                changed = True
            normalized_tags = sorted({
                *task.tags,
                *(tag.strip().lower() for tag in rule.add_tags if tag.strip()),
            })
            if normalized_tags != task.tags:
                task.tags = normalized_tags
                changed = True
            if rule.due_in_days is not None:
                due_date = (current.date() + timedelta(days=rule.due_in_days)).isoformat()
                if task.due_date != due_date:
                    task.due_date = due_date
                    changed = True
            if rule.remind_in_hours is not None:
                remind_at = (current + timedelta(hours=rule.remind_in_hours)).isoformat(timespec="seconds")
                if task.remind_at != remind_at:
                    task.remind_at = remind_at
                    task.snoozed_until = None
                    changed = True
            if changed:
                task.touch()
                applied.append((rule.name, task.id))
    return applied
