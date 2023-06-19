from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class UI_PrivateKeyImportedAlert(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent: QMainWindow = parent
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('Import key')
        self.resize(349, 161)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(90, 120, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.user_label = QtWidgets.QLabel('User', self)
        self.user_label.setGeometry(QtCore.QRect(20, 30, 111, 16))
        self.user_out = QtWidgets.QLabel(self)
        self.user_out.setGeometry(QtCore.QRect(110, 30, 231, 16))
        self.password_label = QtWidgets.QLabel('Password', self)
        self.password_label.setGeometry(QtCore.QRect(20, 90, 60, 16))
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(110, 90, 221, 21))
        self.key_id_label = QtWidgets.QLabel('Key ID', self)
        self.key_id_label.setGeometry(QtCore.QRect(20, 60, 60, 16))
        self.key_id_out = QtWidgets.QLabel(self)
        self.key_id_out.setGeometry(QtCore.QRect(110, 60, 181, 16))


        self.buttonBox.accepted.connect(lambda: print())
        self.buttonBox.rejected.connect(lambda: print())
