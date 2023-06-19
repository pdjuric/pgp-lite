import logging

from PyQt5.QtWidgets import QMainWindow, QListWidgetItem


class QLoggerHandle(logging.Handler):
    def __init__(self, win:QMainWindow):
        super(QLoggerHandle, self).__init__()
        self.widget = win.log.log_list

    def emit(self, record):
        item = QListWidgetItem(self.format(record))
        self.widget.addItem(item)

    def write(self, record):
        pass
