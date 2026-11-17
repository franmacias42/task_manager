from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Possible statuses of a task."""

    PENDING = "Pending"
    COMPLETED = "Completed"


class TaskPriority(Enum):
    """Available priority levels."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass
class Task:
    """Represent a task in the application."""

    title: str
    description: str = ""
    category: str = "General"
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    id: int | None = None

    def complete(self) -> None:
        """Mark the task as completed."""
        self.status = TaskStatus.COMPLETED

    def reopen(self) -> None:
        """Mark the task as pending."""
        self.status = TaskStatus.PENDING
