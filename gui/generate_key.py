from datetime import datetime
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QButtonGroup

from codes import Code
from gui.utils import open_child, back
from gui.key_generated_alert import UI_KeyGeneratedAlert
from pke import PublicKeyAlgorithm
from pke.key import EncryptedPrivateKey
from ring import PrivateRing
from ring.private import PrivateRingEntry


class UI_GenerateKey(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent: QMainWindow = parent
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('Generate Key')
        self.resize(368, 295)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(20, 250, 331, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)


        self.username_label = QtWidgets.QLabel('Username', self)
        self.username_label.setGeometry(QtCore.QRect(10, 20, 81, 16))
        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.setGeometry(QtCore.QRect(150, 20, 201, 21))

        self.email_label = QtWidgets.QLabel('E-mail', self)
        self.email_label.setGeometry(QtCore.QRect(10, 50, 60, 16))
        self.email_input = QtWidgets.QLineEdit(self)
        self.email_input.setGeometry(QtCore.QRect(150, 50, 201, 21))

        self.pka_label = QtWidgets.QLabel('Public Key Algorithm', self)
        self.pka_label.setGeometry(QtCore.QRect(10, 80, 131, 16))

        self.rsa_radio_button = QtWidgets.QRadioButton('RSA', self)
        self.rsa_radio_button.setGeometry(QtCore.QRect(150, 80, 100, 20))
        self.rsa_radio_button.setChecked(True)

        self.dsa_radio_button = QtWidgets.QRadioButton('DSA', self)
        self.dsa_radio_button.setGeometry(QtCore.QRect(150, 100, 100, 20))

        self.elgamal_radio_button = QtWidgets.QRadioButton('ElGamal', self)
        self.elgamal_radio_button.setGeometry(QtCore.QRect(150, 120, 100, 20))

        pka_group = QButtonGroup(self)
        pka_group.addButton(self.rsa_radio_button)
        pka_group.addButton(self.dsa_radio_button)
        pka_group.addButton(self.elgamal_radio_button)

        self.key_size_label = QtWidgets.QLabel('Key size', self)
        self.key_size_label.setGeometry(QtCore.QRect(10, 150, 60, 16))

        self.small_key_size_radio_button = QtWidgets.QRadioButton('1024 bits', self)
        self.small_key_size_radio_button.setGeometry(QtCore.QRect(150, 150, 100, 20))
        self.small_key_size_radio_button.setChecked(True)

        self.big_key_size_radio_button = QtWidgets.QRadioButton('2048 bits', self)
        self.big_key_size_radio_button.setGeometry(QtCore.QRect(150, 170, 100, 20))

        key_size_group = QButtonGroup(self)
        key_size_group.addButton(self.small_key_size_radio_button)
        key_size_group.addButton(self.big_key_size_radio_button)

        self.password_label = QtWidgets.QLabel('Password', self)
        self.password_label.setGeometry(QtCore.QRect(10, 210, 60, 16))
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setGeometry(QtCore.QRect(150, 210, 201, 21))

        def generated():
            user = self.username_input.text() + " <" + self.email_input.text() + ">"
            pka_name = pka_group.checkedButton().text()
            key_size = int(key_size_group.checkedButton().text().split(' ')[0])
            password = self.password_input.text()

            if pka_name == 'RSA':
                code = Code.RSA
            elif pka_name == 'DSA':
                code = Code.DSA
            elif pka_name == 'ElGamal':
                code = Code.ElGamal

            pr, pu = PublicKeyAlgorithm.get_by_code(code).generate_keys(key_size)
            entry = PrivateRingEntry(user, EncryptedPrivateKey(pr, code, bytes(password, 'utf-8')), pu, datetime.now())
            PrivateRing.add(entry)

            self.parent.refresh()
            back(self)
            open_child(self, UI_KeyGeneratedAlert(self, user, pka_name, pu.get_key_ID().hex()))


        self.buttonBox.accepted.connect(generated)
        self.buttonBox.rejected.connect(lambda: back(self))
