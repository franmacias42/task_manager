"""Load realistic example tasks into the application database."""

from pathlib import Path

from app.models.task import Task, TaskPriority, TaskStatus
from app.repositories.sqlite_repository import SQLiteTaskRepository

DEMO_TASKS: list[tuple[str, str, str, TaskPriority, TaskStatus]] = [
    # University
    (
        "Prepare programming project presentation",
        "Create slides and practice the project demonstration.",
        "University",
        TaskPriority.HIGH,
        TaskStatus.PENDING,
    ),
    (
        "Submit laboratory assignment",
        "Complete the exercises and submit the laboratory report.",
        "University",
        TaskPriority.HIGH,
        TaskStatus.COMPLETED,
    ),
    (
        "Review database concepts",
        "Study SQL queries, relationships, and normalization.",
        "University",
        TaskPriority.MEDIUM,
        TaskStatus.PENDING,
    ),
    (
        "Organize lecture notes",
        "Review and organize notes from recent lectures.",
        "University",
        TaskPriority.MEDIUM,
        TaskStatus.COMPLETED,
    ),
    (
        "Read cryptography chapter",
        "Read the assigned textbook sections.",
        "University",
        TaskPriority.LOW,
        TaskStatus.PENDING,
    ),
    (
        "Download course materials",
        "Save the latest lecture presentations and exercises.",
        "University",
        TaskPriority.LOW,
        TaskStatus.COMPLETED,
    ),
    # Projects
    (
        "Finish task manager documentation",
        "Review the README and installation instructions.",
        "Projects",
        TaskPriority.HIGH,
        TaskStatus.PENDING,
    ),
    (
        "Implement repository pattern",
        "Add and test an interchangeable repository implementation.",
        "Projects",
        TaskPriority.HIGH,
        TaskStatus.COMPLETED,
    ),
    (
        "Publish project on GitHub",
        "Create the repository and upload the project files.",
        "Projects",
        TaskPriority.MEDIUM,
        TaskStatus.PENDING,
    ),
    (
        "Write automated tests",
        "Test database operations, CSV export, and concurrency.",
        "Projects",
        TaskPriority.MEDIUM,
        TaskStatus.COMPLETED,
    ),
    (
        "Plan future improvements",
        "Write down possible features for the next version.",
        "Projects",
        TaskPriority.LOW,
        TaskStatus.PENDING,
    ),
    (
        "Organize project folders",
        "Review the folder structure and remove temporary files.",
        "Projects",
        TaskPriority.LOW,
        TaskStatus.COMPLETED,
    ),
    # Personal
    (
        "Buy groceries",
        "Get food and household supplies for the week.",
        "Personal",
        TaskPriority.HIGH,
        TaskStatus.PENDING,
    ),
    (
        "Pay monthly bills",
        "Check and pay the current month's bills.",
        "Personal",
        TaskPriority.HIGH,
        TaskStatus.COMPLETED,
    ),
    (
        "Go to the gym",
        "Complete the planned workout session.",
        "Personal",
        TaskPriority.MEDIUM,
        TaskStatus.PENDING,
    ),
    (
        "Clean apartment",
        "Clean the kitchen, bathroom, and living room.",
        "Personal",
        TaskPriority.MEDIUM,
        TaskStatus.COMPLETED,
    ),
    (
        "Plan weekend activities",
        "Choose activities and places to visit this weekend.",
        "Personal",
        TaskPriority.LOW,
        TaskStatus.PENDING,
    ),
    (
        "Organize personal files",
        "Sort documents and remove unnecessary downloads.",
        "Personal",
        TaskPriority.LOW,
        TaskStatus.COMPLETED,
    ),
    # Work
    (
        "Prepare weekly progress report",
        "Summarize completed tasks and current priorities.",
        "Work",
        TaskPriority.HIGH,
        TaskStatus.PENDING,
    ),
    (
        "Resolve important support request",
        "Investigate and close a high-priority support issue.",
        "Work",
        TaskPriority.HIGH,
        TaskStatus.COMPLETED,
    ),
    (
        "Review team meeting notes",
        "Check meeting decisions and assigned actions.",
        "Work",
        TaskPriority.MEDIUM,
        TaskStatus.PENDING,
    ),
    (
        "Update project documentation",
        "Document recent changes and completed work.",
        "Work",
        TaskPriority.MEDIUM,
        TaskStatus.COMPLETED,
    ),
    (
        "Organize shared documents",
        "Review and categorize files in the shared folder.",
        "Work",
        TaskPriority.LOW,
        TaskStatus.PENDING,
    ),
    (
        "Archive completed reports",
        "Move previous reports into the archive folder.",
        "Work",
        TaskPriority.LOW,
        TaskStatus.COMPLETED,
    ),
]


def main() -> None:
    """Insert demo tasks without creating duplicates."""
    database_path = Path(__file__).resolve().parent / "tasks.db"
    repository = SQLiteTaskRepository(database_path)

    existing_titles = {task.title for task in repository.get_all()}
    added_count = 0

    for title, description, category, priority, status in DEMO_TASKS:
        if title in existing_titles:
            continue

        task = Task(
            title=title,
            description=description,
            category=category,
            priority=priority,
            status=status,
        )

        repository.add(task)
        existing_titles.add(title)
        added_count += 1

    print(f"Added {added_count} demonstration tasks.")
    print(f"Total tasks in database: {len(repository.get_all())}")


if __name__ == "__main__":
    main()
