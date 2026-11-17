import threading
import unittest
from unittest.mock import Mock

from app.gui.main_window import MainWindow


class TestExportConcurrency(unittest.TestCase):
    """Test the background CSV export worker."""

    def setUp(self) -> None:
        """Create simulated dependencies for the export worker."""
        self.mock_window = Mock()

        self.mock_window.export_service = Mock()
        self.mock_window.export_signals = Mock()

    def test_export_runs_in_worker_thread(self) -> None:
        """Verify that the actual worker runs in another thread."""
        main_thread_id = threading.get_ident()
        worker_thread_ids: list[int] = []

        def fake_export(file_name: str) -> int:
            worker_thread_ids.append(threading.get_ident())
            return 3

        self.mock_window.export_service.export.side_effect = fake_export

        worker = threading.Thread(
            target=MainWindow._export_worker,
            args=(self.mock_window, "test.csv"),
            name="TestCSVExportWorker",
        )

        worker.start()
        worker.join(timeout=5)

        self.assertFalse(
            worker.is_alive(),
            "The export thread did not finish.",
        )

        self.assertEqual(len(worker_thread_ids), 1)

        self.assertNotEqual(
            worker_thread_ids[0],
            main_thread_id,
        )

        self.mock_window.export_signals.finished.emit.assert_called_once_with(
            True,
            "Successfully exported 3 tasks.",
        )

    def test_export_worker_reports_success(self) -> None:
        """Verify that a successful export emits a signal."""
        self.mock_window.export_service.export.return_value = 5

        MainWindow._export_worker(
            self.mock_window,
            "test.csv",
        )

        self.mock_window.export_signals.finished.emit.assert_called_once_with(
            True,
            "Successfully exported 5 tasks.",
        )

    def test_export_worker_reports_errors(self) -> None:
        """Verify that export failures emit an error signal."""
        self.mock_window.export_service.export.side_effect = OSError("Disk error")

        MainWindow._export_worker(
            self.mock_window,
            "test.csv",
        )

        self.mock_window.export_signals.finished.emit.assert_called_once_with(
            False,
            "Disk error",
        )


if __name__ == "__main__":
    unittest.main()
