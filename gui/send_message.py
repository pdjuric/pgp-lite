from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QButtonGroup, QFileDialog
from binascii import unhexlify
from codes import Code
from encryption.conversion_step import ConversionStep
from encryption.authentication_step import AuthenticationStep
from encryption.compression_step import CompressionStep
from encryption.encryption_step import EncryptionStep
from encryption.input_step import InputStep
from exceptions import PrivateKeyDecryptionError
from message import Message
from ring import PrivateRing, PublicRing
from ske import AES128
from ske.TripleDES import TripleDES


class UI_SendMessage(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setupUi(self)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("SendMessage")
        MainWindow.resize(532, 379)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 531, 331))
        self.tabWidget.setObjectName("tabWidget")
        self.input_tab = QtWidgets.QWidget()
        self.input_tab.setObjectName("input tab")
        self.input_label = QtWidgets.QLabel(self.input_tab)
        self.input_label.setGeometry(QtCore.QRect(10, 40, 60, 16))
        self.input_label.setObjectName("input label")
        self.plaintext_field = QtWidgets.QTextEdit(self.input_tab)
        self.plaintext_field.setGeometry(QtCore.QRect(80, 40, 431, 231))
        self.plaintext_field.setObjectName("Plaintext")
        self.tabWidget.addTab(self.input_tab, "")

        self.sign_tab = QtWidgets.QWidget()
        self.sign_tab.setObjectName("sign tab")
        self.signature_check_box = QtWidgets.QCheckBox(self.sign_tab)
        self.signature_check_box.setGeometry(QtCore.QRect(20, 20, 87, 20))
        self.signature_check_box.setObjectName("Signature check box")
        self.rsa_radio_button = QtWidgets.QRadioButton(self.sign_tab)
        self.rsa_radio_button.setGeometry(QtCore.QRect(80, 60, 100, 20))
        self.rsa_radio_button.setStatusTip("")
        self.rsa_radio_button.setObjectName("RSA radio button")
        self.rsa_radio_button.setEnabled(False)
        self.dsa_radio_button = QtWidgets.QRadioButton(self.sign_tab)
        self.dsa_radio_button.setGeometry(QtCore.QRect(170, 60, 100, 20))
        self.dsa_radio_button.setObjectName("DSA radio button")
        self.dsa_radio_button.setEnabled(False)
        self.private_key_list = QtWidgets.QListWidget(self.sign_tab)
        self.private_key_list.setGeometry(QtCore.QRect(40, 90, 451, 150))
        self.private_key_list.setObjectName("private key list")
        self.private_key_list.setEnabled(False)
        self.passphrase_label = QtWidgets.QLabel(self.sign_tab)
        self.passphrase_label.setGeometry(QtCore.QRect(40, 250, 100, 30))
        self.passphrase_label.setObjectName("passphrase label")
        self.tabWidget.addTab(self.sign_tab, "")
        self.passphrase_field = QtWidgets.QLineEdit(self.sign_tab)
        self.passphrase_field.setGeometry(QtCore.QRect(170, 250, 100, 30))
        self.passphrase_field.setObjectName("passphrase field")
        self.passphrase_field.setEnabled(False)
        self.tabWidget.addTab(self.sign_tab, "")

        self.signature_check_box.stateChanged.connect(self.signature_state_changed)
        self.rsa_radio_button.clicked.connect(lambda: self.set_private_keys(Code.RSA))
        self.dsa_radio_button.clicked.connect(lambda: self.set_private_keys(Code.DSA))

        self.compress_tab = QtWidgets.QWidget()
        self.compress_tab.setObjectName("compress tab")
        self.compress_check_box = QtWidgets.QCheckBox(self.compress_tab)
        self.compress_check_box.setGeometry(QtCore.QRect(20, 20, 87, 20))
        self.compress_check_box.setObjectName("Compress check box")
        self.tabWidget.addTab(self.compress_tab, "")

        self.encrypt_tab = QtWidgets.QWidget()
        self.encrypt_tab.setObjectName("encrypt tab")
        self.encrypt_check_box = QtWidgets.QCheckBox(self.encrypt_tab)
        self.encrypt_check_box.setGeometry(QtCore.QRect(20, 20, 87, 20))
        self.encrypt_check_box.setObjectName("encrypt check box")
        self.pke_label = QtWidgets.QLabel(self.encrypt_tab)
        self.pke_label.setGeometry(QtCore.QRect(40, 60, 120, 20))
        self.pke_label.setObjectName("ske label")
        self.rsa1_radio_button = QtWidgets.QRadioButton(self.encrypt_tab)
        self.rsa1_radio_button.setGeometry(QtCore.QRect(170, 60, 100, 20))
        self.rsa1_radio_button.setObjectName("RSA1 radio button")
        self.rsa1_radio_button.setEnabled(False)
        self.elgamal_radio_button = QtWidgets.QRadioButton(self.encrypt_tab)
        self.elgamal_radio_button.setGeometry(QtCore.QRect(260, 60, 100, 20))
        self.elgamal_radio_button.setObjectName("elgamal radio button")
        self.elgamal_radio_button.setEnabled(False)
        pke_group = QButtonGroup(self.encrypt_tab)
        pke_group.addButton(self.rsa1_radio_button)
        pke_group.addButton(self.elgamal_radio_button)
        self.public_key_list = QtWidgets.QListWidget(self.encrypt_tab)
        self.public_key_list.setGeometry(QtCore.QRect(40, 90, 451, 150))
        self.public_key_list.setObjectName("public key list")
        self.public_key_list.setEnabled(False)
        self.ske_label = QtWidgets.QLabel(self.encrypt_tab)
        self.ske_label.setGeometry(QtCore.QRect(40, 250, 120, 20))
        self.ske_label.setObjectName("ske label")
        self.aes_radio_button = QtWidgets.QRadioButton(self.encrypt_tab)
        self.aes_radio_button.setGeometry(QtCore.QRect(170, 250, 100, 20))
        self.aes_radio_button.setObjectName("RSA1 radio button")
        self.aes_radio_button.setEnabled(False)
        self.tdes_radio_button = QtWidgets.QRadioButton(self.encrypt_tab)
        self.tdes_radio_button.setGeometry(QtCore.QRect(260, 250, 100, 20))
        self.tdes_radio_button.setObjectName("elgamal radio button")
        self.tdes_radio_button.setEnabled(False)
        ske_group = QButtonGroup(self.encrypt_tab)
        ske_group.addButton(self.aes_radio_button)
        ske_group.addButton(self.tdes_radio_button)
        self.tabWidget.addTab(self.encrypt_tab, "")

        self.encrypt_check_box.stateChanged.connect(self.encrypt_state_changed)
        self.rsa1_radio_button.clicked.connect(lambda: self.set_public_keys(Code.RSA))
        self.elgamal_radio_button.clicked.connect(lambda: self.set_public_keys(Code.ElGamal))

        self.convert_tab = QtWidgets.QWidget()
        self.convert_tab.setObjectName("convert tab")
        self.convert_check_box = QtWidgets.QCheckBox(self.convert_tab)
        self.convert_check_box.setGeometry(QtCore.QRect(20, 20, 87, 20))
        self.convert_check_box.setObjectName("convert check box")
        self.tabWidget.addTab(self.convert_tab, "")

        self.send_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_button.setGeometry(QtCore.QRect(210, 340, 113, 32))
        self.send_button.setObjectName("sendButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.send_button.clicked.connect(self.send)


    def signature_state_changed(self):
        signature_state = self.signature_check_box.isChecked()
        self.rsa_radio_button.setEnabled(signature_state)
        self.dsa_radio_button.setEnabled(signature_state)
        self.private_key_list.setEnabled(signature_state)
        self.passphrase_field.setEnabled(signature_state)


    def encrypt_state_changed(self):
        encrypt_state = self.encrypt_check_box.isChecked()
        self.rsa1_radio_button.setEnabled(encrypt_state)
        self.elgamal_radio_button.setEnabled(encrypt_state)
        self.aes_radio_button.setEnabled(encrypt_state)
        self.tdes_radio_button.setEnabled(encrypt_state)
        self.public_key_list.setEnabled(encrypt_state)


    def set_private_keys(self, code:Code):
        self.private_key_list.clear()
        for entry in PrivateRing.get_by_pka_code(code):
            item = QtWidgets.QListWidgetItem(entry.user + " [" + entry.public_key.get_key_ID().hex() + "]")
            self.private_key_list.addItem(item)


    def set_public_keys(self, code:Code):
        self.public_key_list.clear()
        for entry in PublicRing.get_by_pka_code(code):
            item = QtWidgets.QListWidgetItem(entry.user + " [" + entry.public_key.get_key_ID().hex() + "]")
            self.public_key_list.addItem(item)


    def send(self):
        msg = self.plaintext_field.toPlainText()
        message = Message("")
        InputStep(bytes(msg, 'utf-8')).execute(message)
        if self.signature_check_box.isChecked():
            if self.private_key_list.currentItem():
                item = self.private_key_list.currentItem().text()
                start_index = item.find('[')
                end_index = item.rfind(']')
                key_id = unhexlify(item[start_index + 1:end_index])
                private_key_entry = PrivateRing.get_by_key_ID(key_id)
                passphrase = bytes(self.passphrase_field.text(), 'utf-8')
                try:
                    private_key = private_key_entry.get_private_key(passphrase)
                except PrivateKeyDecryptionError as e:
                    ret = QMessageBox.question(self, 'Alert', "Passcode is incorrect",
                                               QMessageBox.Cancel,
                                               QMessageBox.Cancel)
                    return

                AuthenticationStep(private_key).execute(message)
            else:
                ret = QMessageBox.question(self, 'Alert', "Private key must be selected",
                                           QMessageBox.Cancel,
                                           QMessageBox.Cancel)
                return

        if self.compress_check_box.isChecked():
            CompressionStep().execute(message)

        if self.encrypt_check_box.isChecked():
            if self.aes_radio_button.isChecked() or self.tdes_radio_button.isChecked():
                if self.public_key_list.currentItem():
                    item = self.public_key_list.currentItem().text()
                    start_index = item.find('[')
                    end_index = item.rfind(']')
                    key_id = unhexlify(item[start_index + 1:end_index])
                    public_key_entry = PublicRing.get_by_key_ID(key_id)
                    public_key = public_key_entry.public_key
                    if self.aes_radio_button.isChecked():
                        ske_algorithm = AES128()
                    else:
                        ske_algorithm = TripleDES()

                    EncryptionStep(public_key, ske_algorithm).execute(message)
                else:
                    ret = QMessageBox.question(self, 'Alert', "Public key must be selected",
                                               QMessageBox.Cancel,
                                               QMessageBox.Cancel)
                    return
            else:
                ret = QMessageBox.question(self, 'Alert', "Symetric key algorithm must be selected",
                                           QMessageBox.Cancel,
                                           QMessageBox.Cancel)
                return

        if self.convert_check_box.isChecked():
            ConversionStep().execute(message)

        if self.encrypt_check_box.isChecked() and self.signature_check_box.isChecked():
            if not ((self.rsa_radio_button.isChecked() and self.rsa1_radio_button.isChecked())
                or (self.dsa_radio_button.isChecked() and self.elgamal_radio_button)):
                ret = QMessageBox.question(self, 'Alert', "Only cobinations RSA&RSA and DSA&Elgamal are supported",
                                           QMessageBox.Cancel,
                                           QMessageBox.Cancel)
                return
        file = QFileDialog.getSaveFileName(self, 'Save Message')
        if file:
            with open(file[0]+'.txt', 'wb') as file:
                file.write(message.get_bytes(0))
            self.parent.show()
            self.hide()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Send a Message"))
        self.input_label.setText(_translate("MainWindow", "Message"))
        self.passphrase_label.setText(_translate("MainWindow", "Passphrase"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.input_tab), _translate("MainWindow", "Input"))
        self.signature_check_box.setText(_translate("MainWindow", "Enable"))
        self.rsa_radio_button.setText(_translate("MainWindow", "RSA"))
        self.dsa_radio_button.setText(_translate("MainWindow", "DSA"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sign_tab), _translate("MainWindow", "Sign"))
        self.compress_check_box.setText(_translate("MainWindow", "Enable"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.compress_tab), _translate("MainWindow", "Compress"))
        self.pke_label.setText(_translate("MainWindow", "Public Key Algorithm:"))
        self.encrypt_check_box.setText(_translate("MainWindow", "Enable"))
        self.rsa1_radio_button.setText(_translate("MainWindow", "RSA"))
        self.ske_label.setText(_translate("MainWindow", "Symetric Key Algorithm:"))
        self.elgamal_radio_button.setText(_translate("MainWindow", "El Gamal"))
        self.aes_radio_button.setText(_translate("MainWindow", "AES128"))
        self.tdes_radio_button.setText(_translate("MainWindow", "TripleDes"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.encrypt_tab), _translate("MainWindow", "Encrypt"))
        self.convert_check_box.setText(_translate("MainWindow", "Enable"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.convert_tab), _translate("MainWindow", "Convert to radix64"))
        self.send_button.setText(_translate("MainWindow", "Send"))
