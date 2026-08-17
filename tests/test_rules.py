import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from flowpilot.models import Task
from flowpilot.rules import Rule, apply_rules, load_rules, preview_rules


NOW = datetime(2030, 1, 10, 9, 0, tzinfo=timezone.utc)


def test_rule_matches_multiple_conditions_and_sets_actions() -> None:
    task = Task("Send client report", priority="medium", tags=["client"])
    rule = Rule(
        "prepare client work",
        match_priority="medium",
        match_tag="client",
        title_contains="report",
        set_priority="high",
        add_tags=("review", "Client"),
        due_in_days=2,
        remind_in_hours=24,
    )

    applied = apply_rules([task], [rule], now=NOW)

    assert applied == [("prepare client work", task.id)]
    assert task.priority == "high"
    assert task.tags == ["client", "review"]
    assert task.due_date == "2030-01-12"
    assert task.remind_at == "2030-01-11T09:00:00+00:00"


def test_rules_skip_nonmatching_and_inactive_tasks() -> None:
    tasks = [
        Task("Personal note", tags=["personal"]),
        Task("Completed report", completed=True, tags=["client"]),
        Task("Archived report", archived=True, tags=["client"]),
    ]
    rule = Rule("client work", match_tag="client", set_priority="high")

    assert apply_rules(tasks, [rule], now=NOW) == []
    assert all(task.priority == "medium" for task in tasks)


def test_rule_application_reports_only_real_changes() -> None:
    task = Task("Already urgent", priority="high", tags=["review"])
    rule = Rule("mark urgent", set_priority="high", add_tags=("review",))

    assert apply_rules([task], [rule], now=NOW) == []


def test_load_rules_parses_json_file(tmp_path: Path) -> None:
    path = tmp_path / "rules.json"
    path.write_text(json.dumps([
        {
            "name": "urgent work",
            "match_tag": "urgent",
            "set_priority": "high",
            "add_tags": ["review"],
        }
    ]), encoding="utf-8")

    rules = load_rules(path)

    assert rules == [
        Rule(
            "urgent work",
            match_tag="urgent",
            set_priority="high",
            add_tags=("review",),
        )
    ]


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "not a list"},
        [{"set_priority": "high"}],
        [{"name": "bad", "unknown": True}],
        [{"name": "bad", "add_tags": "review"}],
        [{"name": "bad", "set_priority": "urgent"}],
        [{"name": "bad", "due_in_days": -1}],
    ],
)
def test_load_rules_rejects_unsafe_or_invalid_shapes(tmp_path: Path, payload: object) -> None:
    path = tmp_path / "rules.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError):
        load_rules(path)


def test_rule_exclusions_prevent_unwanted_matches() -> None:
    tasks = [
        Task("Send internal report", tags=["client", "internal"]),
        Task("Send draft report", tags=["client"]),
        Task("Send final report", tags=["client"]),
    ]
    rule = Rule(
        "published client reports",
        match_tag="client",
        exclude_tag="internal",
        exclude_title_contains="draft",
        set_priority="high",
    )

    applied = apply_rules(tasks, [rule], now=NOW)

    assert applied == [("published client reports", tasks[2].id)]
    assert [task.priority for task in tasks] == ["medium", "medium", "high"]


def test_load_rules_accepts_exclusion_fields(tmp_path: Path) -> None:
    path = tmp_path / "rules.json"
    path.write_text(json.dumps([{
        "name": "external only",
        "exclude_tag": "internal",
        "exclude_title_contains": "draft",
        "set_priority": "high",
    }]), encoding="utf-8")

    rule = load_rules(path)[0]

    assert rule.exclude_tag == "internal"
    assert rule.exclude_title_contains == "draft"


def test_rule_can_clear_due_date_and_reminder() -> None:
    task = Task(
        "Unscheduled work",
        due_date="2030-02-01",
        remind_at="2030-01-31T09:00:00+00:00",
        snoozed_until="2030-01-31T11:00:00+00:00",
    )
    rule = Rule("remove schedule", clear_due_date=True, clear_reminder=True)

    applied = apply_rules([task], [rule], now=NOW)

    assert applied == [("remove schedule", task.id)]
    assert task.due_date is None
    assert task.remind_at is None
    assert task.snoozed_until is None


@pytest.mark.parametrize(
    "rule",
    [
        Rule,
    ],
)
def test_rule_rejects_conflicting_schedule_actions(rule: type[Rule]) -> None:
    with pytest.raises(ValueError, match="clear and set a due date"):
        rule("conflict", due_in_days=1, clear_due_date=True)
    with pytest.raises(ValueError, match="clear and set a reminder"):
        rule("conflict", remind_in_hours=1, clear_reminder=True)


def test_preview_rules_reports_changes_without_mutating_tasks() -> None:
    task = Task("Client report", tags=["client"])
    before = task.to_dict()
    rule = Rule("prioritize clients", match_tag="client", set_priority="high")

    planned = preview_rules([task], [rule], now=NOW)

    assert planned == [("prioritize clients", task.id)]
    assert task.to_dict() == before


def test_load_rules_rejects_duplicate_names_case_insensitively(tmp_path: Path) -> None:
    path = tmp_path / "rules.json"
    path.write_text(json.dumps([
        {"name": "Urgent Work", "set_priority": "high"},
        {"name": " urgent work ", "add_tags": ["focus"]},
    ]), encoding="utf-8")

    with pytest.raises(ValueError, match="unique"):
        load_rules(path)
