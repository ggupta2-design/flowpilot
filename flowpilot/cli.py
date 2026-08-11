import argparse
from pathlib import Path

from .analytics import completion_stats
from .csvio import export_tasks
from .filtering import filter_tasks
from .formatting import format_json, format_task
from .models import Task
from .store import TaskStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="flowpilot")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="Create a task")
    add.add_argument("title")
    add.add_argument("--priority", choices=["low", "medium", "high"], default="medium")
    add.add_argument("--due", dest="due_date", help="Due date in YYYY-MM-DD format")

    listing = commands.add_parser("list", help="List tasks")
    listing.add_argument("--status", choices=["all", "open", "done"], default="all")
    listing.add_argument("--search")
    listing.add_argument("--json", action="store_true", dest="as_json")

    for name in ("complete", "delete"):
        command = commands.add_parser(name, help=f"{name.title()} a task")
        command.add_argument("task_id")

    commands.add_parser("stats", help="Show progress summary")
    export = commands.add_parser("export", help="Export tasks to CSV")
    export.add_argument("path", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = TaskStore()
    tasks = store.load()

    if args.command == "add":
        task = Task(args.title, priority=args.priority, due_date=args.due_date)
        tasks.append(task)
        store.save(tasks)
        print(f"Created {task.id}: {task.title}")
    elif args.command == "list":
        visible = filter_tasks(tasks, status=args.status, search=args.search)
        print(format_json(visible) if args.as_json else "\n".join(map(format_task, visible)) or "No tasks.")
    elif args.command in {"complete", "delete"}:
        task = next((item for item in tasks if item.id == args.task_id), None)
        if task is None:
            print(f"Task not found: {args.task_id}")
            return 1
        if args.command == "complete":
            task.completed = True
            print(f"Completed {task.id}: {task.title}")
        else:
            tasks.remove(task)
            print(f"Deleted {task.id}")
        store.save(tasks)
    elif args.command == "stats":
        stats = completion_stats(tasks)
        print(" | ".join(f"{key.title()}: {value}" for key, value in stats.items()))
    elif args.command == "export":
        count = export_tasks(tasks, args.path)
        print(f"Exported {count} tasks to {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
