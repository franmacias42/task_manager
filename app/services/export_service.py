import csv
from pathlib import Path

from app.repositories.task_protocol import TaskRepositoryProtocol


class CSVExportService:
    """Export stored tasks to a CSV file."""

    def __init__(self, repository: TaskRepositoryProtocol) -> None:
        self.repository = repository

    def export(self, file_path: str | Path) -> int:
        """Export all tasks and return the number exported."""
        tasks = self.repository.get_all()
        path = Path(file_path)

        with path.open(
            mode="w",
            newline="",
            encoding="utf-8-sig",
        ) as csv_file:
            writer = csv.writer(
                csv_file,
                delimiter=";",
            )

            writer.writerow(
                [
                    "ID",
                    "Title",
                    "Description",
                    "Category",
                    "Priority",
                    "Status",
                    "Created At",
                ]
            )

            for task in tasks:
                writer.writerow(
                    [
                        task.id,
                        task.title,
                        task.description,
                        task.category,
                        task.priority.value,
                        task.status.value,
                        task.created_at.isoformat(),
                    ]
                )

        return len(tasks)
