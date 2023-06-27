from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow

from gui.private_keys import UI_PrivateKeys
from gui.public_keys import UI_PublicKeys
from gui.receive_message import UI_ReceiveMessage
from gui.send_message import UI_SendMessage
from gui.utils import open_child


class UI_PGPlite(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("PGP lite")
        self.resize(464, 205)
        self.setAcceptDrops(False)
        self.centralwidget = QtWidgets.QWidget(self)
        self.private_keys = QtWidgets.QPushButton('Private Keys', self.centralwidget)
        self.private_keys.setGeometry(QtCore.QRect(30, 40, 181, 51))
        self.public_keys = QtWidgets.QPushButton('Public Keys', self.centralwidget)
        self.public_keys.setGeometry(QtCore.QRect(30, 120, 181, 51))
        self.send_message = QtWidgets.QPushButton('Send Message', self.centralwidget)
        self.send_message.setGeometry(QtCore.QRect(250, 40, 181, 51))
        self.receive_message = QtWidgets.QPushButton('Receive Message', self.centralwidget)
        self.receive_message.setGeometry(QtCore.QRect(250, 120, 181, 51))
        self.setCentralWidget(self.centralwidget)

        self.setTabOrder(self.private_keys, self.public_keys)
        self.setTabOrder(self.public_keys, self.send_message)
        self.setTabOrder(self.send_message, self.receive_message)

        self.private_keys.clicked.connect(lambda: open_child(self, UI_PrivateKeys(self)))
        self.public_keys.clicked.connect(lambda: open_child(self, UI_PublicKeys(self)))
        self.send_message.clicked.connect(lambda: open_child(self, UI_SendMessage(self)))
        self.receive_message.clicked.connect(lambda: UI_ReceiveMessage(self).show())
