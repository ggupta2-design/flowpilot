from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .models import Task
from .rules import Rule, apply_rules


AUDITED_FIELDS = (
    "priority",
    "tags",
    "due_date",
    "remind_at",
    "snoozed_until",
)


@dataclass(frozen=True, slots=True)
class RuleChange:
    rule_name: str
    task_id: str
    task_title: str
    before: dict[str, Any]
    after: dict[str, Any]

    @property
    def changed_fields(self) -> tuple[str, ...]:
        return tuple(
            field
            for field in AUDITED_FIELDS
            if self.before[field] != self.after[field]
        )

    def to_dict(self) -> dict[str, Any]:
        fields = self.changed_fields
        return {
            "rule": self.rule_name,
            "task_id": self.task_id,
            "task_title": self.task_title,
            "changed_fields": list(fields),
            "before": {field: self.before[field] for field in fields},
            "after": {field: self.after[field] for field in fields},
        }


def _snapshot(task: Task) -> dict[str, Any]:
    return {field: getattr(task, field) for field in AUDITED_FIELDS}


def audit_rules(
    tasks: list[Task],
    rules: list[Rule],
    *,
    now: datetime | None = None,
) -> list[RuleChange]:
    """Explain sequential rule effects without mutating the source tasks."""
    working = [Task.from_dict(task.to_dict()) for task in tasks]
    changes: list[RuleChange] = []

    for task in working:
        for rule in rules:
            before = _snapshot(task)
            if not apply_rules([task], [rule], now=now):
                continue
            after = _snapshot(task)
            changes.append(
                RuleChange(
                    rule_name=rule.name,
                    task_id=task.id,
                    task_title=task.title,
                    before=before,
                    after=after,
                )
            )
    return changes


def format_audit_text(changes: list[RuleChange]) -> str:
    if not changes:
        return "No rule changes."
    lines: list[str] = []
    for change in changes:
        details = ", ".join(
            f"{field}: {change.before[field]!r} -> {change.after[field]!r}"
            for field in change.changed_fields
        )
        lines.append(
            f"{change.rule_name} -> {change.task_id} ({change.task_title}): {details}"
        )
    return "\n".join(lines)
