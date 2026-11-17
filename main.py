import logging
import sys

from PySide6.QtWidgets import QApplication

from app.gui.main_window import MainWindow


def main() -> None:
    """Start the Task Management desktop application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
