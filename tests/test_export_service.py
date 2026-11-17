import csv
import tempfile
import unittest
from pathlib import Path

from app.models.task import Task, TaskPriority, TaskStatus
from app.repositories.sqlite_repository import SQLiteTaskRepository
from app.services.export_service import CSVExportService


class TestCSVExportService(unittest.TestCase):
    """Automated tests for CSV export."""

    def setUp(self) -> None:
        """Prepare an isolated database and export service."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)

        self.repository = SQLiteTaskRepository(self.folder / "test_tasks.db")
        self.service = CSVExportService(self.repository)
        self.csv_path = self.folder / "export.csv"

    def tearDown(self) -> None:
        """Delete temporary test files."""
        self.temp_dir.cleanup()

    def read_csv(self) -> list[dict[str, str]]:
        """Read the exported CSV file."""
        with self.csv_path.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:
            return list(csv.DictReader(file, delimiter=";"))

    def test_export_empty_database(self) -> None:
        """An empty database produces a CSV with headers."""
        count = self.service.export(self.csv_path)

        self.assertEqual(count, 0)
        self.assertTrue(self.csv_path.exists())
        self.assertEqual(self.read_csv(), [])

    def test_export_multiple_tasks(self) -> None:
        """All stored tasks must be exported."""
        self.repository.add(Task("Task One"))
        self.repository.add(Task("Task Two"))

        count = self.service.export(self.csv_path)
        rows = self.read_csv()

        self.assertEqual(count, 2)
        self.assertEqual(len(rows), 2)

        titles = {row["Title"] for row in rows}
        self.assertEqual(titles, {"Task One", "Task Two"})

    def test_export_preserves_task_data(self) -> None:
        """Priority, category and status are preserved."""
        task = Task(
            title="Important university task",
            description="Complete the project",
            category="University",
            priority=TaskPriority.HIGH,
            status=TaskStatus.COMPLETED,
        )

        self.repository.add(task)
        self.service.export(self.csv_path)

        row = self.read_csv()[0]

        self.assertEqual(row["Title"], task.title)
        self.assertEqual(row["Description"], task.description)
        self.assertEqual(row["Category"], "University")
        self.assertEqual(row["Priority"], "High")
        self.assertEqual(row["Status"], "Completed")

    def test_export_csv_columns(self) -> None:
        """Verify that all seven columns are present."""
        self.repository.add(Task("Example"))
        self.service.export(self.csv_path)

        row = self.read_csv()[0]

        expected_columns = [
            "ID",
            "Title",
            "Description",
            "Category",
            "Priority",
            "Status",
            "Created At",
        ]

        self.assertEqual(list(row.keys()), expected_columns)


if __name__ == "__main__":
    unittest.main()
