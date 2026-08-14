# FlowPilot

FlowPilot is a lightweight command-line assistant for organizing recurring work and personal automations.

## Why FlowPilot?

Recurring responsibilities are easy to lose across notes, calendars, and spreadsheets. FlowPilot keeps them in one local, scriptable workflow without requiring an account or cloud database.

## Features

- Create and edit tasks with priorities, due dates, normalized tags, and effort estimates
- Attach timezone-aware reminder timestamps and query reminders that are ready
- Build a deadline-aware daily agenda within a time budget
- Complete and reopen work without losing its history
- Archive and restore tasks instead of deleting them
- Detect overdue work and track active, archived, and remaining-work metrics
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
flowpilot edit TASK_ID --estimate 45 --clear-reminder
flowpilot agenda --capacity 240 --date 2030-01-01
flowpilot reminders --at 2029-12-31T17:00:00-05:00
flowpilot complete TASK_ID
flowpilot reopen TASK_ID
flowpilot archive TASK_ID
flowpilot list --archived
flowpilot restore TASK_ID
flowpilot stats
pytest
```

Reminder timestamps must include a UTC offset such as `Z`, `+00:00`, or `-05:00`. FlowPilot evaluates them locally and does not send data to an external notification service.

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
| `complete` / `reopen` | Reversibly change completion state |
| `archive` / `restore` | Hide or restore inactive tasks |
| `delete` | Permanently remove a task |
| `repeat` | Create the next daily, weekly, or monthly occurrence |
| `stats` | Summarize active, overdue, archived, and remaining work |
| `export` / `import` | Transfer tasks through CSV |
| `backup` / `restore-backup` | Transfer versioned JSON backups |
| `recover` | Restore the previous automatic local snapshot |

Task data is stored at `~/.flowpilot/tasks.json`; the previous version is retained at `tasks.json.bak`. See [SECURITY.md](SECURITY.md) before handling sensitive information.
