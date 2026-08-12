# FlowPilot

FlowPilot is a lightweight command-line assistant for organizing recurring work and personal automations.

## Why FlowPilot?

Recurring responsibilities are easy to lose across notes, calendars, and spreadsheets. FlowPilot keeps them in one local, scriptable workflow without requiring an account or cloud database.

## Features

- Create tasks with priorities, due dates, and normalized tags
- Detect overdue work and track completion metrics
- Search, filter, and sort tasks by status, priority, tag, creation time, or deadline
- Generate the next daily, weekly, or monthly occurrence of a task
- Import and export task data through CSV
- Produce machine-readable JSON output
- Store data safely using atomic local writes with clear corruption errors

## Quick start

```bash
python -m pip install -e ".[dev]"

flowpilot add "Send weekly report" --priority high --due 2030-01-01 --tag work --tag weekly
flowpilot list --status open --tag work --sort due
flowpilot stats
flowpilot export reports/tasks.csv
flowpilot import reports/tasks.csv
pytest
```

To create the next occurrence of a dated task:

```bash
flowpilot repeat TASK_ID weekly
```

You can also run the package directly:

```bash
python -m flowpilot list
```

## Commands

| Command | Purpose |
|---|---|
| `add` | Create a prioritized, tagged task with an optional due date |
| `list` | Search, filter, sort, or return JSON |
| `complete` | Mark a task finished |
| `delete` | Remove a task |
| `repeat` | Create the next daily, weekly, or monthly occurrence |
| `stats` | Summarize completion and overdue progress |
| `export` | Write tasks to a portable CSV file |
| `import` | Safely merge tasks from a CSV file |

Task data is stored at `~/.flowpilot/tasks.json`. See [SECURITY.md](SECURITY.md) before handling sensitive task information.
