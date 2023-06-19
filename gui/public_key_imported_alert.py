from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QButtonGroup

from gui.generate_key import back
from ring.public import Trust


class UI_PublicKeyImportedAlert(QDialog):

    def __init__(self, parent, username, key_ID, trust, callback):
        super().__init__(parent)
        self.trust = trust
        self.callback = callback

        self.setWindowTitle('Import key')
        self.resize(349, 202)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(90, 160, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)

        self.user_label = QtWidgets.QLabel('User', self)
        self.user_label.setGeometry(QtCore.QRect(20, 30, 111, 16))
        self.username_label_out = QtWidgets.QLabel(username, self)
        self.username_label_out.setGeometry(QtCore.QRect(110, 30, 231, 16))

        self.owner_trust_label = QtWidgets.QLabel('Owner Trust', self)
        self.owner_trust_label.setGeometry(QtCore.QRect(20, 90, 81, 16))

        self.key_id_label = QtWidgets.QLabel('Key ID', self)
        self.key_id_label.setGeometry(QtCore.QRect(20, 60, 60, 16))
        self.key_id_out = QtWidgets.QLabel(key_ID.hex(), self)
        self.key_id_out.setGeometry(QtCore.QRect(110, 60, 181, 16))

        self.trusted = QtWidgets.QRadioButton('Trusted', self)
        self.trusted.setGeometry(QtCore.QRect(110, 90, 100, 20))
        self.partially_trusted = QtWidgets.QRadioButton('Partially Trusted', self)
        self.partially_trusted.setGeometry(QtCore.QRect(110, 110, 131, 20))
        self.not_trusted = QtWidgets.QRadioButton('Not Trusted', self)
        self.not_trusted.setGeometry(QtCore.QRect(110, 130, 100, 20))
        self.not_trusted.setChecked(True)

        self.radio_group = QButtonGroup()
        self.radio_group.addButton(self.trusted)
        self.radio_group.addButton(self.partially_trusted)
        self.radio_group.addButton(self.not_trusted)

        self.trust_out = QtWidgets.QLabel(self)
        self.trust_out.setGeometry(QtCore.QRect(110, 90, 150, 16))

        def r():
            if self.trust == Trust.UNKNOWN:
                if self.radio_group.checkedButton().text() == "Trusted":
                    self.callback(Trust.FULL_TRUST)
                elif self.radio_group.checkedButton().text() == "Partially Trusted":
                    self.callback(Trust.PARTIAL_TRUST)
                else:
                    self.callback(Trust.NO_TRUST)
            back(self)


        self.buttonBox.accepted.connect(lambda: r())

        if trust == Trust.UNKNOWN:
            self.trust_out.hide()
        else:
            self.trust_out.setText(str(trust))
            self.trusted.hide()
            self.partially_trusted.hide()
            self.not_trusted.hide()

