from typing import Protocol

from app.models.task import Task


class TaskRepositoryProtocol(Protocol):
    """Define the required operations for task storage."""

    def add(self, task: Task) -> Task:
        """Save a new task."""
        ...

    def get_all(self) -> list[Task]:
        """Retrieve all stored tasks."""
        ...

    def get_by_id(self, task_id: int) -> Task | None:
        """Find a task using its ID."""
        ...

    def update(self, task: Task) -> bool:
        """Update an existing task."""
        ...

    def delete(self, task_id: int) -> bool:
        """Delete a task."""
        ...
