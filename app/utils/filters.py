from collections.abc import Callable

from app.models.task import Task, TaskPriority, TaskStatus


def create_task_filter(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
) -> Callable[[Task], bool]:
    """Create a task filter using a closure.

    The returned function remembers the selected filters.

    >>> from app.models.task import Task
    >>> pending = create_task_filter(status=TaskStatus.PENDING)
    >>> pending(Task("Study Python"))
    True
    >>> completed = Task("Finished work")
    >>> completed.complete()
    >>> pending(completed)
    False
    """

    def matches(task: Task) -> bool:
        """Check whether a task matches the selected filters."""
        if status is not None and task.status != status:
            return False

        return priority is None or task.priority == priority

    return matches


def filter_tasks(
    tasks: list[Task],
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
) -> list[Task]:
    """Return tasks matching the specified filters."""
    predicate = create_task_filter(status, priority)
    return [task for task in tasks if predicate(task)]
