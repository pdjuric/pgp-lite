from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog


class UI_PasswordPrompt(QDialog):
    def __init__(self, parent, key_text, submit_password_callback):
        super().__init__(parent)
        self.key_text = key_text
        self.submit_password_callback = submit_password_callback
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('Enter Password')
        self.resize(341, 163)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(90, 120, 151, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.label = QtWidgets.QLabel('Enter password for ' + self.key_text, self)
        self.label.setGeometry(QtCore.QRect(40, 20, 261, 41))
        self.label.setWordWrap(True)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(50, 80, 241, 21))

        def return_password(password):
            if self.submit_password_callback(password):
                self.close()

        self.buttonBox.accepted.connect(lambda: return_password(self.lineEdit.text()))
        self.buttonBox.rejected.connect(lambda: self.close())
        QtCore.QMetaObject.connectSlotsByName(self)


def enter_password(func):
    from custom_logger import log_handler
    p = UI_PasswordPrompt(log_handler.widget, 'key', lambda x: func(x))
    p.exec_()
