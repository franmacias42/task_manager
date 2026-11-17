
import logging
import sys
import threading
import time

from PySide6.QtWidgets import QApplication

from app.gui.main_window import MainWindow


def main() -> None:
    """Run a manual GUI responsiveness test."""
    logging.basicConfig(level=logging.INFO)

    app = QApplication(sys.argv)
    window = MainWindow()

    original_export = window.export_service.export

    def slow_export(file_name: str) -> int:
        """Simulate a slow export operation."""
        print(
            "Export started in thread:",
            threading.get_ident(),
            flush=True,
        )
        time.sleep(5)
        return original_export(file_name)

    window.export_service.export = slow_export

    print(
        "Main thread:",
        threading.get_ident(),
        flush=True,
    )

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
