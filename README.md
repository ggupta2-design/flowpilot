# FlowPilot

FlowPilot is a lightweight command-line assistant for organizing recurring work and personal automations.

## Why FlowPilot?

Recurring responsibilities are easy to lose across notes, calendars, and spreadsheets. FlowPilot keeps them in one local, scriptable workflow without requiring an account or cloud database.

## Features

- Create tasks with low, medium, or high priority
- Assign and validate due dates
- Detect overdue work
- Search and filter open or completed tasks
- Track completion and overdue metrics
- Export task data to JSON or CSV
- Store data safely using atomic local writes

## Quick start

```bash
python -m pip install -e ".[dev]"
flowpilot add "Send weekly report" --priority high --due 2030-01-01
flowpilot list --status open
flowpilot stats
flowpilot export reports/tasks.csv
pytest
```

You can also run the package directly:

```bash
python -m flowpilot list
```

## Commands

| Command | Purpose |
|---|---|
| `add` | Create a prioritized task with an optional due date |
| `list` | Filter, search, or return JSON |
| `complete` | Mark a task finished |
| `delete` | Remove a task |
| `stats` | Summarize completion and overdue progress |
| `export` | Create a portable CSV file |

Task data is stored at `~/.flowpilot/tasks.json`. See [SECURITY.md](SECURITY.md) before handling sensitive task information.
