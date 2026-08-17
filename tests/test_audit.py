from datetime import datetime, timezone

from flowpilot.audit import RuleChange, audit_rules, format_audit_text
from flowpilot.models import Task
from flowpilot.rules import Rule


NOW = datetime(2030, 1, 10, 9, 0, tzinfo=timezone.utc)


def test_audit_rules_explains_each_changed_field() -> None:
    task = Task("Client report", priority="medium", tags=["client"])
    rule = Rule(
        "prepare client work",
        match_tag="client",
        set_priority="high",
        add_tags=("review",),
        due_in_days=2,
    )

    changes = audit_rules([task], [rule], now=NOW)

    assert len(changes) == 1
    change = changes[0]
    assert change.rule_name == "prepare client work"
    assert change.task_id == task.id
    assert change.changed_fields == ("priority", "tags", "due_date")
    assert change.to_dict()["before"] == {
        "priority": "medium",
        "tags": ["client"],
        "due_date": None,
    }
    assert change.to_dict()["after"] == {
        "priority": "high",
        "tags": ["client", "review"],
        "due_date": "2030-01-12",
    }


def test_audit_does_not_mutate_source_tasks() -> None:
    task = Task("Urgent work", tags=["urgent"])
    before = task.to_dict()

    audit_rules(
        [task],
        [Rule("prioritize", match_tag="urgent", set_priority="high")],
        now=NOW,
    )

    assert task.to_dict() == before


def test_audit_preserves_sequential_rule_effects() -> None:
    task = Task("Report", priority="medium")
    rules = [
        Rule("raise", set_priority="high"),
        Rule("label high", match_priority="high", add_tags=("review",)),
    ]

    changes = audit_rules([task], rules, now=NOW)

    assert [change.rule_name for change in changes] == ["raise", "label high"]
    assert changes[1].changed_fields == ("tags",)


def test_rule_change_serializes_only_changed_values() -> None:
    change = RuleChange(
        "priority",
        "task-1",
        "Report",
        {
            "priority": "medium",
            "tags": [],
            "due_date": None,
            "remind_at": None,
            "snoozed_until": None,
        },
        {
            "priority": "high",
            "tags": [],
            "due_date": None,
            "remind_at": None,
            "snoozed_until": None,
        },
    )

    assert change.to_dict()["changed_fields"] == ["priority"]


def test_audit_text_names_rule_task_and_field_changes() -> None:
    task = Task("Client report", tags=["client"])
    changes = audit_rules(
        [task],
        [Rule("prioritize", match_tag="client", set_priority="high")],
        now=NOW,
    )

    output = format_audit_text(changes)

    assert "prioritize" in output
    assert task.id in output
    assert "Client report" in output
    assert "priority: 'medium' -> 'high'" in output


def test_empty_audit_has_clear_message() -> None:
    assert format_audit_text([]) == "No rule changes."
