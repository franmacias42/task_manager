import threading
from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.gui.task_dialog import TaskDialog
from app.models.task import TaskPriority, TaskStatus
from app.repositories.sqlite_repository import SQLiteTaskRepository
from app.services.export_service import CSVExportService
from app.services.export_signals import ExportSignals
from app.utils.filters import filter_tasks


class MainWindow(QMainWindow):
    """Main window of the Task Management Application."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Task Management Application")
        self.resize(1000, 650)

        # Database configuration
        database_path = Path(__file__).resolve().parents[2] / "tasks.db"
        self.repository = SQLiteTaskRepository(database_path)

        # CSV export service and concurrency
        self.export_service = CSVExportService(self.repository)
        self.export_signals = ExportSignals()

        self.export_signals.finished.connect(self.on_export_finished)

        self._export_thread: threading.Thread | None = None
        self._exporting: bool = False

        # Main window layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        title = QLabel("My Task Manager")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(title)

        # Action buttons
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Task")
        self.edit_button = QPushButton("Edit Task")
        self.delete_button = QPushButton("Delete Task")
        self.complete_button = QPushButton("Complete / Reopen")
        self.refresh_button = QPushButton("Refresh")
        self.export_button = QPushButton("Export to CSV")

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.complete_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.export_button)

        layout.addLayout(button_layout)

        # Task filtering controls
        filter_layout = QHBoxLayout()

        status_label = QLabel("Status:")
        self.status_filter = QComboBox()
        self.status_filter.addItem("All", None)

        for status in TaskStatus:
            self.status_filter.addItem(
                status.value,
                status,
            )

        priority_label = QLabel("Priority:")
        self.priority_filter = QComboBox()
        self.priority_filter.addItem("All", None)

        for priority in TaskPriority:
            self.priority_filter.addItem(
                priority.value,
                priority,
            )

        filter_layout.addWidget(status_label)
        filter_layout.addWidget(self.status_filter)
        filter_layout.addWidget(priority_label)
        filter_layout.addWidget(self.priority_filter)

        layout.addLayout(filter_layout)

        # Task table
        self.table = QTableWidget()
        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels(
            ["ID", "Title", "Category", "Priority", "Status"]
        )

        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        layout.addWidget(self.table)

        self.setCentralWidget(central_widget)

        # Button connections
        self.refresh_button.clicked.connect(self.load_tasks)
        self.add_button.clicked.connect(self.add_task)
        self.edit_button.clicked.connect(self.edit_task)
        self.delete_button.clicked.connect(self.delete_task)

        self.complete_button.clicked.connect(self.toggle_task_status)

        self.export_button.clicked.connect(self.export_tasks)

        # Filter connections
        self.status_filter.currentIndexChanged.connect(self.load_tasks)

        self.priority_filter.currentIndexChanged.connect(self.load_tasks)

        # Load tasks when starting the application
        self.load_tasks()

    def load_tasks(self) -> None:
        """Load and filter stored tasks into the table."""
        tasks = self.repository.get_all()

        selected_status = self.status_filter.currentData()
        selected_priority = self.priority_filter.currentData()

        filtered_tasks = filter_tasks(
            tasks,
            status=selected_status,
            priority=selected_priority,
        )

        self.table.setRowCount(len(filtered_tasks))

        for row, task in enumerate(filtered_tasks):
            values = [
                str(task.id),
                task.title,
                task.category,
                task.priority.value,
                task.status.value,
            ]

            for column, value in enumerate(values):
                self.table.setItem(
                    row,
                    column,
                    QTableWidgetItem(value),
                )

        self.table.resizeColumnsToContents()

        self.table.horizontalHeader().setStretchLastSection(True)

    def add_task(self) -> None:
        """Open a dialog and save a new task."""
        dialog = TaskDialog(self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            task = dialog.get_task()
            self.repository.add(task)
            self.load_tasks()

    def get_selected_task_id(self) -> int | None:
        """Return the ID of the selected task."""
        selected_row = self.table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(
                self,
                "No Task Selected",
                "Please select a task first.",
            )
            return None

        id_item = self.table.item(selected_row, 0)

        if id_item is None:
            return None

        return int(id_item.text())

    def edit_task(self) -> None:
        """Edit the selected task."""
        task_id = self.get_selected_task_id()

        if task_id is None:
            return

        task = self.repository.get_by_id(task_id)

        if task is None:
            QMessageBox.warning(
                self,
                "Task Not Found",
                "The selected task no longer exists.",
            )
            self.load_tasks()
            return

        dialog = TaskDialog(self, task)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_task = dialog.get_task()
            self.repository.update(updated_task)
            self.load_tasks()

    def delete_task(self) -> None:
        """Delete the selected task after confirmation."""
        task_id = self.get_selected_task_id()

        if task_id is None:
            return

        confirmation = QMessageBox.question(
            self,
            "Delete Task",
            "Are you sure you want to delete this task?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            self.repository.delete(task_id)
            self.load_tasks()

    def toggle_task_status(self) -> None:
        """Toggle a task between pending and completed."""
        task_id = self.get_selected_task_id()

        if task_id is None:
            return

        task = self.repository.get_by_id(task_id)

        if task is None:
            QMessageBox.warning(
                self,
                "Task Not Found",
                "The selected task no longer exists.",
            )
            self.load_tasks()
            return

        if task.status == TaskStatus.PENDING:
            task.complete()
        else:
            task.reopen()

        self.repository.update(task)
        self.load_tasks()

    def export_tasks(self) -> None:
        """Choose a file and start a background CSV export."""
        if self._exporting:
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Export Tasks",
            "tasks_export.csv",
            "CSV Files (*.csv)",
        )

        if not file_name:
            return

        self._exporting = True
        self.export_button.setEnabled(False)
        self.export_button.setText("Exporting...")

        self._export_thread = threading.Thread(
            target=self._export_worker,
            args=(file_name,),
            name="CSVExportWorker",
        )

        self._export_thread.start()

    def _export_worker(self, file_name: str) -> None:
        """Export tasks using a background thread."""
        try:
            count = self.export_service.export(file_name)
        except Exception as error:  # noqa: BLE001
            self.export_signals.finished.emit(
                False,
                str(error),
            )
        else:
            self.export_signals.finished.emit(
                True,
                f"Successfully exported {count} tasks.",
            )

    @Slot(bool, str)
    def on_export_finished(
        self,
        success: bool,
        message: str,
    ) -> None:
        """Handle export results in the GUI thread."""
        if self._export_thread is not None:
            self._export_thread.join()

        self._export_thread = None
        self._exporting = False

        self.export_button.setEnabled(True)
        self.export_button.setText("Export to CSV")

        if success:
            QMessageBox.information(
                self,
                "Export Complete",
                message,
            )
        else:
            QMessageBox.critical(
                self,
                "Export Error",
                message,
            )

    def closeEvent(self, event: QCloseEvent) -> None:
        """Prevent closing during an active CSV export."""
        if self._exporting:
            QMessageBox.warning(
                self,
                "Export in Progress",
                "Please finish the export before closing.",
            )
            event.ignore()
            return

        super().closeEvent(event)
