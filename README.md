# FlowPilot

FlowPilot is a lightweight command-line assistant for organizing recurring work and personal automations.

## Why FlowPilot?

Recurring responsibilities are easy to lose across notes, calendars, and spreadsheets. FlowPilot keeps them in one local, scriptable workflow without requiring an account or cloud database.

## Features

- Create and edit tasks with priorities, due dates, normalized tags, and effort estimates
- Attach timezone-aware reminders, snooze alerts, and query reminders that are ready
- Apply deterministic JSON automation rules without executing arbitrary code
- Build a deadline-aware daily agenda within a time budget
- Complete, reopen, archive, and restore work without losing its history
- Track overdue work, remaining effort, and scheduled or ready reminders
- Search, filter, and sort tasks by status, priority, tag, creation time, or deadline
- Generate the next daily, weekly, or monthly occurrence
- Import and export task data through CSV
- Create and restore versioned JSON backups
- Recover the previous local store after an accidental overwrite
- Store data safely using atomic writes and automatic recovery snapshots

## Quick start

```bash
python -m pip install -e ".[dev]"

flowpilot add "Send weekly report" --priority high --due 2030-01-01 --tag work \
  --estimate 60 --remind-at 2029-12-31T16:00:00-05:00
flowpilot agenda --capacity 240 --date 2030-01-01
flowpilot reminders --at 2029-12-31T17:00:00-05:00
flowpilot snooze TASK_ID 2029-12-31T19:00:00-05:00
flowpilot unsnooze TASK_ID
flowpilot complete TASK_ID
flowpilot stats
pytest
```

Reminder and snooze timestamps must include a UTC offset such as `Z`, `+00:00`, or `-05:00`. FlowPilot evaluates them locally and does not send data to an external notification service.

## Automation rules

Rules are JSON objects with explicit matching and action fields. Supported matches are `match_priority`, `match_tag`, and `title_contains`. Supported actions are `set_priority`, `add_tags`, `due_in_days`, and `remind_in_hours`.

```json
[
  {
    "name": "prepare client reports",
    "match_tag": "client",
    "title_contains": "report",
    "set_priority": "high",
    "add_tags": ["review"],
    "due_in_days": 2,
    "remind_in_hours": 24
  }
]
```

Preview the rule file, then apply it at the current time:

```bash
flowpilot apply-rules examples/rules.json
```

Rules skip completed and archived tasks. Reapplying a rule records only real changes, and unknown fields are rejected.

## Recurrence and portability

```bash
flowpilot repeat TASK_ID weekly
flowpilot export reports/tasks.csv
flowpilot import reports/tasks.csv
flowpilot backup backups/flowpilot.json
flowpilot restore-backup backups/flowpilot.json
flowpilot recover
```

## Commands

| Command | Purpose |
|---|---|
| `add` / `edit` | Create or revise a task and its planning metadata |
| `list` | Search, filter, sort, or return JSON |
| `agenda` | Select deadline-aware tasks that fit a time budget |
| `reminders` | Show ready reminders as text or JSON |
| `snooze` / `unsnooze` | Defer or restore a reminder |
| `apply-rules` | Apply validated task automation rules from JSON |
| `complete` / `reopen` | Reversibly change completion state |
| `archive` / `restore` | Hide or restore inactive tasks |
| `delete` | Permanently remove a task |
| `repeat` | Create the next daily, weekly, or monthly occurrence |
| `stats` | Summarize active, overdue, archived, effort, and reminder metrics |
| `export` / `import` | Transfer tasks through CSV |
| `backup` / `restore-backup` | Transfer versioned JSON backups |
| `recover` | Restore the previous automatic local snapshot |

Task data is stored at `~/.flowpilot/tasks.json`; the previous version is retained at `tasks.json.bak`. See [SECURITY.md](SECURITY.md) before handling sensitive information.
