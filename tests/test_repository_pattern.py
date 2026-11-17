import csv
import tempfile
import unittest
from pathlib import Path

from app.models.task import Task
from app.services.export_service import CSVExportService


class InMemoryTaskRepository:
    """Simple in-memory repository used for testing."""

    def __init__(self) -> None:
        self.tasks: list[Task] = []

    def add(self, task: Task) -> Task:
        task.id = len(self.tasks) + 1
        self.tasks.append(task)
        return task

    def get_all(self) -> list[Task]:
        return list(self.tasks)

    def get_by_id(self, task_id: int) -> Task | None:
        return next(
            (task for task in self.tasks if task.id == task_id),
            None,
        )

    def update(self, task: Task) -> bool:
        for index, stored_task in enumerate(self.tasks):
            if stored_task.id == task.id:
                self.tasks[index] = task
                return True
        return False

    def delete(self, task_id: int) -> bool:
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                return True
        return False


class TestRepositoryPattern(unittest.TestCase):
    """Verify that services can use interchangeable repositories."""

    def test_export_with_in_memory_repository(self) -> None:
        """CSV export works without using SQLite."""
        repository = InMemoryTaskRepository()
        repository.add(Task(title="Repository pattern example"))

        service = CSVExportService(repository)

        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "tasks.csv"

            count = service.export(csv_path)

            with csv_path.open(
                encoding="utf-8-sig",
                newline="",
            ) as csv_file:
                rows = list(csv.DictReader(csv_file, delimiter=";"))

        self.assertEqual(count, 1)
        self.assertEqual(len(rows), 1)
        self.assertEqual(
            rows[0]["Title"],
            "Repository pattern example",
        )


if __name__ == "__main__":
    unittest.main()
