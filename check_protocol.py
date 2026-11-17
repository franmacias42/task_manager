from app.repositories.sqlite_repository import SQLiteTaskRepository
from app.repositories.task_protocol import TaskRepositoryProtocol


def count_tasks(repository: TaskRepositoryProtocol) -> int:
    """Count tasks through the repository protocol."""
    return len(repository.get_all())


def verify_repository(
    repository: SQLiteTaskRepository,
) -> int:
    """Verify structural compatibility using static typing."""
    protocol_repository: TaskRepositoryProtocol = repository
    return count_tasks(protocol_repository)
