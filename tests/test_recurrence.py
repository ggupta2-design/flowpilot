import pytest

from flowpilot.recurrence import next_due_date


@pytest.mark.parametrize(
    ("due", "frequency", "expected"),
    [
        ("2030-01-15", "daily", "2030-01-16"),
        ("2030-01-15", "weekly", "2030-01-22"),
        ("2030-01-31", "monthly", "2030-02-28"),
        ("2032-01-31", "monthly", "2032-02-29"),
        ("2030-12-31", "monthly", "2031-01-31"),
    ],
)
def test_next_due_date(due: str, frequency: str, expected: str) -> None:
    assert next_due_date(due, frequency) == expected


def test_invalid_frequency() -> None:
    with pytest.raises(ValueError, match="Frequency"):
        next_due_date("2030-01-01", "yearly")
