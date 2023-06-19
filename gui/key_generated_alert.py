from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog


class UI_KeyGeneratedAlert(QDialog):

    def __init__(self, parent, username, pka, key_ID):
        super().__init__(parent)
        self.setWindowTitle('Generated Key')
        self.resize(422, 165)
        self.label = QtWidgets.QLabel('User', self)
        self.label.setGeometry(QtCore.QRect(20, 30, 60, 16))
        self.label_2 = QtWidgets.QLabel(username, self)
        self.label_2.setGeometry(QtCore.QRect(160, 30, 241, 20))
        self.label_3 = QtWidgets.QLabel('Public Key Algorithm', self)
        self.label_3.setGeometry(QtCore.QRect(20, 60, 131, 16))
        self.label_4 = QtWidgets.QLabel('Key ID', self)
        self.label_4.setGeometry(QtCore.QRect(20, 90, 60, 16))
        self.label_5 = QtWidgets.QLabel(pka, self)
        self.label_5.setGeometry(QtCore.QRect(160, 60, 201, 16))
        self.label_6 = QtWidgets.QLabel(key_ID, self)
        self.label_6.setGeometry(QtCore.QRect(160, 90, 241, 16))
        self.pushButton = QtWidgets.QPushButton('OK', self)
        self.pushButton.setGeometry(QtCore.QRect(150, 120, 113, 32))

        self.pushButton.clicked.connect(lambda: self.hide())

