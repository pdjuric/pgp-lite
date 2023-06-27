import logging
from typing import Optional

from PyQt5.QtWidgets import QListWidgetItem, QListWidget


class QLoggerHandle(logging.Handler):
    def __init__(self):
        super(QLoggerHandle, self).__init__()
        self.widget: Optional[QListWidget] = None

    def emit(self, record):
        item = QListWidgetItem(self.format(record))
        self.widget.addItem(item)

    def write(self, record):
        pass


log_handler = QLoggerHandle()
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)