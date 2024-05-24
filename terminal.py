from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCharFormat, QColor

class Terminal(QTextEdit):
    """
    Terminal on the GUI
    """

    def __init__(self, parent=None):
        """
        Initialize the Terminal widget
        """
        super().__init__(parent)
        self.setReadOnly(True)

    def write(self, message, message_type="stdout"):
        """
        Write message to the terminal
        :param message: str, message to display
        :param message_type: str, type of message ("stdout" or "stderr")
        """
        format = QTextCharFormat()
        if message_type == "stderr":
            format.setForeground(QColor("red"))
        else:
            format.setForeground(QColor("black"))

        self.setCurrentCharFormat(format)
        self.append(message)
        self.moveCursor(self.textCursor().End)

    def flush(self):
        """
        Required method to handle stdout redirection
        """
        pass
