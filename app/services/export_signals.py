from PySide6.QtCore import QObject, Signal


class ExportSignals(QObject):
    """Communicate export results to the GUI thread."""

    finished = Signal(bool, str)
