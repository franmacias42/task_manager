import tempfile
import unittest
from pathlib import Path

from app.models.task import Task, TaskStatus
from app.repositories.sqlite_repository import SQLiteTaskRepository


class TestSQLiteTaskRepository(unittest.TestCase):
    """Test SQLite task repository operations."""

    def setUp(self) -> None:
        """Create an isolated database for each test."""
        self.temp_dir = tempfile.TemporaryDirectory()
        database_path = Path(self.temp_dir.name) / "test_tasks.db"
        self.repository = SQLiteTaskRepository(database_path)

    def tearDown(self) -> None:
        """Remove the temporary test database."""
        self.temp_dir.cleanup()

    def test_add_task(self) -> None:
        """Test creating a new task."""
        task = Task("Study Python")

        saved_task = self.repository.add(task)

        self.assertIsNotNone(saved_task.id)
        self.assertEqual(saved_task.title, "Study Python")

    def test_get_all_tasks(self) -> None:
        """Test retrieving all tasks."""
        self.repository.add(Task("Task 1"))
        self.repository.add(Task("Task 2"))

        tasks = self.repository.get_all()

        self.assertEqual(len(tasks), 2)

    def test_get_task_by_id(self) -> None:
        """Test retrieving a task using its ID."""
        task = self.repository.add(Task("Find me"))

        assert task.id is not None
        found_task = self.repository.get_by_id(task.id)

        assert found_task is not None
        self.assertEqual(found_task.title, "Find me")

    def test_update_task(self) -> None:
        """Test updating an existing task."""
        task = self.repository.add(Task("Original"))

        task.title = "Updated"
        result = self.repository.update(task)

        self.assertTrue(result)
        assert task.id is not None

        updated_task = self.repository.get_by_id(task.id)

        assert updated_task is not None
        self.assertEqual(updated_task.title, "Updated")

    def test_delete_task(self) -> None:
        """Test deleting a task."""
        task = self.repository.add(Task("Delete me"))

        assert task.id is not None
        result = self.repository.delete(task.id)

        self.assertTrue(result)
        self.assertIsNone(self.repository.get_by_id(task.id))

    def test_complete_task(self) -> None:
        """Test saving a completed task."""
        task = self.repository.add(Task("Complete me"))

        task.complete()
        self.repository.update(task)

        assert task.id is not None
        saved_task = self.repository.get_by_id(task.id)

        assert saved_task is not None
        self.assertEqual(
            saved_task.status,
            TaskStatus.COMPLETED,
        )


if __name__ == "__main__":
    unittest.main()
