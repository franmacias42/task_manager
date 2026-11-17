import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from app.models.task import Task, TaskPriority, TaskStatus
from app.repositories.base_repository import TaskRepository
from app.utils.decorators import measure_execution_time


class SQLiteTaskRepository(TaskRepository):
    """SQLite implementation of the task repository."""

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = str(database_path)
        self._create_table()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        """Open, commit or roll back, and close a connection."""
        connection = sqlite3.connect(self.database_path)

        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def _create_table(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    category TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

    @staticmethod
    def _row_to_task(row: tuple) -> Task:
        return Task(
            id=row[0],
            title=row[1],
            description=row[2],
            category=row[3],
            priority=TaskPriority(row[4]),
            status=TaskStatus(row[5]),
            created_at=datetime.fromisoformat(row[6]),
        )

    @measure_execution_time
    def add(self, task: Task) -> Task:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO tasks (
                    title, description, category,
                    priority, status, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    task.title,
                    task.description,
                    task.category,
                    task.priority.value,
                    task.status.value,
                    task.created_at.isoformat(),
                ),
            )
            task.id = cursor.lastrowid

        return task

    @measure_execution_time
    def get_all(self) -> list[Task]:
        with self._connect() as connection:
            rows = connection.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()

        return [self._row_to_task(row) for row in rows]

    @measure_execution_time
    def get_by_id(self, task_id: int) -> Task | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM tasks WHERE id = ?",
                (task_id,),
            ).fetchone()

        return self._row_to_task(row) if row else None

    @measure_execution_time
    def update(self, task: Task) -> bool:
        if task.id is None:
            return False

        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE tasks
                SET title = ?, description = ?, category = ?,
                    priority = ?, status = ?
                WHERE id = ?
                """,
                (
                    task.title,
                    task.description,
                    task.category,
                    task.priority.value,
                    task.status.value,
                    task.id,
                ),
            )

        return cursor.rowcount > 0

    @measure_execution_time
    def delete(self, task_id: int) -> bool:
        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM tasks WHERE id = ?",
                (task_id,),
            )

        return cursor.rowcount > 0
