from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QTextEdit,
)

from app.models.task import Task, TaskPriority


class TaskDialog(QDialog):
    """Dialog for creating and editing tasks."""

    def __init__(
        self,
        parent=None,
        task: Task | None = None,
    ) -> None:
        super().__init__(parent)

        self.task = task

        if task is None:
            self.setWindowTitle("Add New Task")
        else:
            self.setWindowTitle("Edit Task")

        self.resize(400, 300)

        layout = QFormLayout(self)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter task title")

        self.description_input = QTextEdit()

        self.category_input = QLineEdit()
        self.category_input.setText("General")

        self.priority_input = QComboBox()

        for priority in TaskPriority:
            self.priority_input.addItem(
                priority.value,
                priority,
            )

        self.priority_input.setCurrentIndex(
            self.priority_input.findData(TaskPriority.MEDIUM)
        )

        layout.addRow("Title:", self.title_input)
        layout.addRow("Description:", self.description_input)
        layout.addRow("Category:", self.category_input)
        layout.addRow("Priority:", self.priority_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)

        if task is not None:
            self.title_input.setText(task.title)
            self.description_input.setPlainText(task.description)
            self.category_input.setText(task.category)

            index = self.priority_input.findData(task.priority)
            self.priority_input.setCurrentIndex(index)

    def accept(self) -> None:
        """Validate task information."""
        if not self.title_input.text().strip():
            self.title_input.setFocus()
            return

        super().accept()

    def get_task(self) -> Task:
        """Return the created or edited task."""
        if self.task is None:
            task = Task(title=self.title_input.text().strip())
        else:
            task = self.task

        task.title = self.title_input.text().strip()
        task.description = self.description_input.toPlainText()
        task.category = self.category_input.text().strip() or "General"
        task.priority = self.priority_input.currentData()

        return task
