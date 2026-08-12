import argparse
from pathlib import Path

from .analytics import completion_stats
from .csvio import export_tasks, import_tasks
from .filtering import filter_tasks
from .formatting import format_json, format_task
from .models import Task
from .recurrence import FREQUENCIES, next_due_date
from .sorting import sort_tasks
from .store import TaskStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="flowpilot")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="Create a task")
    add.add_argument("title")
    add.add_argument("--priority", choices=["low", "medium", "high"], default="medium")
    add.add_argument("--due", dest="due_date", help="Due date in YYYY-MM-DD format")
    add.add_argument("--tag", action="append", default=[], dest="tags")

    listing = commands.add_parser("list", help="List tasks")
    listing.add_argument("--status", choices=["all", "open", "done"], default="all")
    listing.add_argument("--search")
    listing.add_argument("--priority", choices=["low", "medium", "high"])
    listing.add_argument("--tag")
    listing.add_argument("--sort", choices=["created", "priority", "due"], default="created")
    listing.add_argument("--json", action="store_true", dest="as_json")

    for name in ("complete", "delete"):
        command = commands.add_parser(name, help=f"{name.title()} a task")
        command.add_argument("task_id")

    repeat = commands.add_parser("repeat", help="Create the next recurring task")
    repeat.add_argument("task_id")
    repeat.add_argument("frequency", choices=sorted(FREQUENCIES))

    commands.add_parser("stats", help="Show progress summary")

    export = commands.add_parser("export", help="Export tasks to CSV")
    export.add_argument("path", type=Path)

    importing = commands.add_parser("import", help="Import tasks from CSV")
    importing.add_argument("path", type=Path)
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
        )
        visible = sort_tasks(visible, args.sort)
        print(format_json(visible) if args.as_json else "\n".join(map(format_task, visible)) or "No tasks.")
    elif args.command in {"complete", "delete", "repeat"}:
        task = _find_task(tasks, args.task_id)
        if task is None:
            print(f"Task not found: {args.task_id}")
            return 1
        if args.command == "complete":
            task.completed = True
            print(f"Completed {task.id}: {task.title}")
        elif args.command == "delete":
            tasks.remove(task)
            print(f"Deleted {task.id}")
        else:
            if not task.due_date:
                print(f"Task has no due date: {task.id}")
                return 1
            repeated = Task(
                task.title,
                priority=task.priority,
                due_date=next_due_date(task.due_date, args.frequency),
                tags=task.tags,
            )
            tasks.append(repeated)
            print(f"Created recurring task {repeated.id} due {repeated.due_date}")
        store.save(tasks)
    elif args.command == "stats":
        stats = completion_stats(tasks)
        print(" | ".join(f"{key.title()}: {value}" for key, value in stats.items()))
    elif args.command == "export":
        count = export_tasks(tasks, args.path)
        print(f"Exported {count} tasks to {args.path}")
    elif args.command == "import":
        incoming = import_tasks(args.path)
        existing_ids = {task.id for task in tasks}
        duplicates = {task.id for task in incoming if task.id in existing_ids}
        if duplicates:
            print(f"Import contains existing task IDs: {', '.join(sorted(duplicates))}")
            return 1
        tasks.extend(incoming)
        store.save(tasks)
        print(f"Imported {len(incoming)} tasks from {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
