import logging
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from custom_logger import QLoggerHandle
from gui.private_keys import PrivateKeys
from gui.receive_message import UI_ReceiveMessage
from gui.send_message import UI_SendMessage

class UI_PGPlite(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = UI_ReceiveMessage(self)
        self.setupUi(self)


    def setupUi(self, PGPlite):
        PGPlite.setObjectName("PGPlite")
        PGPlite.resize(464, 205)
        PGPlite.setAcceptDrops(False)
        self.centralwidget = QtWidgets.QWidget(PGPlite)
        self.centralwidget.setObjectName("centralwidget")
        self.private_keys = QtWidgets.QPushButton(self.centralwidget)
        self.private_keys.setGeometry(QtCore.QRect(30, 40, 181, 51))
        self.private_keys.setObjectName("private_keys")
        self.import_key = QtWidgets.QPushButton(self.centralwidget)
        self.import_key.setGeometry(QtCore.QRect(30, 120, 181, 51))
        self.import_key.setObjectName("import_key")
        self.send_message = QtWidgets.QPushButton(self.centralwidget)
        self.send_message.setGeometry(QtCore.QRect(250, 40, 181, 51))
        self.send_message.setObjectName("send_message")
        self.receive_message = QtWidgets.QPushButton(self.centralwidget)
        self.receive_message.setGeometry(QtCore.QRect(250, 120, 181, 51))
        self.receive_message.setObjectName("receive_message")
        PGPlite.setCentralWidget(self.centralwidget)

        self.retranslateUi(PGPlite)
        QtCore.QMetaObject.connectSlotsByName(PGPlite)
        PGPlite.setTabOrder(self.private_keys, self.import_key)
        PGPlite.setTabOrder(self.import_key, self.send_message)
        PGPlite.setTabOrder(self.send_message, self.receive_message)

        self.private_keys.clicked.connect(self.open_private_keys)
        self.send_message.clicked.connect(self.open_send_message)
        self.receive_message.clicked.connect(self.open_receive_message)


    def open_private_keys(self):
        self.w = PrivateKeys(self)
        self.w.show()
        self.hide()


    def open_send_message(self):
        self.w = UI_SendMessage(self)
        self.w.show()
        self.hide()


    def open_receive_message(self):
        self.log.log_list.clear()
        self.w = self.log
        self.w.show()
        self.hide()

    def retranslateUi(self, PGPlite):
        _translate = QtCore.QCoreApplication.translate
        PGPlite.setWindowTitle(_translate("PGPlite", "PGP lite"))
        self.private_keys.setText(_translate("PGPlite", "Private Keys"))
        self.import_key.setText(_translate("PGPlite", "Public Keys"))
        self.send_message.setText(_translate("PGPlite", "Send Message"))
        self.receive_message.setText(_translate("PGPlite", "Receive Message"))

def enter_password(func) :
    from gui.password_prompt import UI_PasswordPrompt

    p = UI_PasswordPrompt(win.log, '', lambda x: func(x))
    p.exec_()


app = QApplication(sys.argv)
win = UI_PGPlite()

log_handler = QLoggerHandle(win)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

win.show()
sys.exit(app.exec())
