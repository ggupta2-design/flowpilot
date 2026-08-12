from .models import Task


def filter_tasks(
    tasks: list[Task],
    *,
    status: str = "all",
    search: str | None = None,
    priority: str | None = None,
    tag: str | None = None,
) -> list[Task]:
    if status not in {"all", "open", "done"}:
        raise ValueError("Status must be all, open, or done")
    if priority and priority not in {"low", "medium", "high"}:
        raise ValueError("Priority must be low, medium, or high")

    result = list(tasks)
    if status == "open":
        result = [task for task in result if not task.completed]
    elif status == "done":
        result = [task for task in result if task.completed]
    if search:
        query = search.casefold()
        result = [task for task in result if query in task.title.casefold()]
    if priority:
        result = [task for task in result if task.priority == priority]
    if tag:
        normalized_tag = tag.strip().lower()
        result = [task for task in result if normalized_tag in task.tags]
    return result
