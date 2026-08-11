from .models import Task


def filter_tasks(
    tasks: list[Task],
    *,
    status: str = "all",
    search: str | None = None,
) -> list[Task]:
    if status not in {"all", "open", "done"}:
        raise ValueError("Status must be all, open, or done")
    result = list(tasks)
    if status == "open":
        result = [task for task in result if not task.completed]
    elif status == "done":
        result = [task for task in result if task.completed]
    if search:
        query = search.casefold()
        result = [task for task in result if query in task.title.casefold()]
    return result
