from pathlib import Path

from flowpilot.cli import build_parser


def test_apply_rules_parser_supports_dry_run_and_fixed_time() -> None:
    args = build_parser().parse_args([
        "apply-rules",
        "rules.json",
        "--dry-run",
        "--explain",
        "--at",
        "2030-01-10T09:00:00+00:00",
    ])

    assert args.command == "apply-rules"
    assert args.path == Path("rules.json")
    assert args.dry_run
    assert args.explain
    assert args.current_time == "2030-01-10T09:00:00+00:00"


def test_validate_rules_parser_accepts_a_rules_file() -> None:
    args = build_parser().parse_args(["validate-rules", "automation.json"])

    assert args.command == "validate-rules"
    assert args.path == Path("automation.json")
