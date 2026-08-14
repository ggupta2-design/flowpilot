import argparse
from datetime import date, datetime
from pathlib import Path

from .analytics import completion_stats
from .backup import create_backup, merge_backup, read_backup
from .csvio import export_tasks, import_tasks
from .filtering import filter_tasks
from .formatting import format_json, format_task
from .models import Task
from .operations import archive_task, complete_task, edit_task, reopen_task, restore_task
from .planner import build_daily_plan, planned_minutes
from .recurrence import FREQUENCIES, next_due_date
from .reminders import reminders_ready
from .sorting import sort_tasks
from .store import TaskStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="flowpilot")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="Create a task")
    add.add_argument("title")
    add.add_argument("--priority", choices=["low", "medium", "high"], default="medium")
    add.add_argument("--due", dest="due_date")
    add.add_argument("--tag", action="append", default=[], dest="tags")
    add.add_argument("--estimate", type=int, default=30, dest="estimated_minutes")
    add.add_argument("--remind-at")

    listing = commands.add_parser("list", help="List tasks")
    listing.add_argument("--status", choices=["all", "open", "done"], default="all")
    listing.add_argument("--search")
    listing.add_argument("--priority", choices=["low", "medium", "high"])
    listing.add_argument("--tag")
    listing.add_argument("--archived", action="store_true")
    listing.add_argument("--sort", choices=["created", "priority", "due"], default="created")
    listing.add_argument("--json", action="store_true", dest="as_json")

    for name in ("complete", "reopen", "archive", "restore", "delete"):
        command = commands.add_parser(name, help=f"{name.title()} a task")
        command.add_argument("task_id")

    edit = commands.add_parser("edit", help="Edit task fields")
    edit.add_argument("task_id")
    edit.add_argument("--title")
    edit.add_argument("--priority", choices=["low", "medium", "high"])
    edit.add_argument("--due", dest="due_date")
    edit.add_argument("--clear-due", action="store_true")
    edit.add_argument("--tag", action="append", dest="tags")
    edit.add_argument("--estimate", type=int, dest="estimated_minutes")
    edit.add_argument("--remind-at")
    edit.add_argument("--clear-reminder", action="store_true")

    repeat = commands.add_parser("repeat", help="Create the next recurring task")
    repeat.add_argument("task_id")
    repeat.add_argument("frequency", choices=sorted(FREQUENCIES))

    agenda = commands.add_parser("agenda", help="Build a capacity-aware daily plan")
    agenda.add_argument("--capacity", type=int, default=480)
    agenda.add_argument("--date", dest="plan_date")

    reminders = commands.add_parser("reminders", help="Show reminders ready now")
    reminders.add_argument("--at", dest="current_time")
    reminders.add_argument("--json", action="store_true", dest="as_json")

    commands.add_parser("stats", help="Show progress summary")
    for name in ("export", "import", "backup", "restore-backup"):
        command = commands.add_parser(name)
        command.add_argument("path", type=Path)
    commands.add_parser("recover", help="Recover the previous local store")
    return parser


def _find_task(tasks: list[Task], task_id: str) -> Task | None:
    return next((item for item in tasks if item.id == task_id), None)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = TaskStore()
    tasks = store.load()

    if args.command == "add":
        task = Task(
            args.title,
            priority=args.priority,
            due_date=args.due_date,
            tags=args.tags,
            estimated_minutes=args.estimated_minutes,
            remind_at=args.remind_at,
        )
        tasks.append(task)
        store.save(tasks)
        print(f"Created {task.id}: {task.title}")
    elif args.command == "list":
        visible = filter_tasks(
            tasks,
            status=args.status,
            search=args.search,
            priority=args.priority,
            tag=args.tag,
            archived=args.archived,
        )
        visible = sort_tasks(visible, args.sort)
        print(format_json(visible) if args.as_json else "\n".join(map(format_task, visible)) or "No tasks.")
    elif args.command in {"complete", "reopen", "archive", "restore", "delete", "edit", "repeat"}:
        task = _find_task(tasks, args.task_id)
        if task is None:
            print(f"Task not found: {args.task_id}")
            return 1
        if args.command == "complete":
            complete_task(task)
        elif args.command == "reopen":
            reopen_task(task)
        elif args.command == "archive":
            archive_task(task)
        elif args.command == "restore":
            restore_task(task)
        elif args.command == "delete":
            tasks.remove(task)
        elif args.command == "edit":
            edit_task(
                task,
                title=args.title,
                priority=args.priority,
                due_date=args.due_date,
                clear_due_date=args.clear_due,
                tags=args.tags,
                estimated_minutes=args.estimated_minutes,
                remind_at=args.remind_at,
                clear_reminder=args.clear_reminder,
            )
        else:
            if not task.due_date:
                print(f"Task has no due date: {task.id}")
                return 1
            tasks.append(Task(
                task.title,
                priority=task.priority,
                due_date=next_due_date(task.due_date, args.frequency),
                tags=task.tags,
                estimated_minutes=task.estimated_minutes,
            ))
        store.save(tasks)
        print(f"{args.command.title()} succeeded for {task.id}")
    elif args.command == "agenda":
        target = date.fromisoformat(args.plan_date) if args.plan_date else None
        plan = build_daily_plan(tasks, args.capacity, plan_date=target)
        print(f"Planned {planned_minutes(plan)} of {args.capacity} minutes")
        print("\n".join(map(format_task, plan)) or "No tasks fit the plan.")
    elif args.command == "reminders":
        current = datetime.fromisoformat(args.current_time) if args.current_time else None
        ready = reminders_ready(tasks, now=current)
        print(format_json(ready) if args.as_json else "\n".join(map(format_task, ready)) or "No reminders.")
    elif args.command == "stats":
        stats = completion_stats(tasks)
        print(" | ".join(f"{key.title()}: {value}" for key, value in stats.items()))
    elif args.command == "export":
        print(f"Exported {export_tasks(tasks, args.path)} tasks to {args.path}")
    elif args.command == "import":
        tasks = merge_backup(tasks, import_tasks(args.path))
        store.save(tasks)
        print(f"Imported tasks from {args.path}")
    elif args.command == "backup":
        print(f"Backed up {create_backup(tasks, args.path)} tasks to {args.path}")
    elif args.command == "restore-backup":
        tasks = merge_backup(tasks, read_backup(args.path))
        store.save(tasks)
        print(f"Restored tasks from {args.path}")
    elif args.command == "recover":
        print(f"Recovered {len(store.recover())} tasks from {store.recovery_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
