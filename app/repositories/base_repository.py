from abc import ABC, abstractmethod

from app.models.task import Task


class TaskRepository(ABC):
    """Abstract interface for task persistence."""

    @abstractmethod
    def add(self, task: Task) -> Task:
        """Save a new task."""

    @abstractmethod
    def get_all(self) -> list[Task]:
        """Retrieve all tasks."""

    @abstractmethod
    def get_by_id(self, task_id: int) -> Task | None:
        """Retrieve a task by its identifier."""

    @abstractmethod
    def update(self, task: Task) -> bool:
        """Update an existing task."""

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        """Delete an existing task."""
