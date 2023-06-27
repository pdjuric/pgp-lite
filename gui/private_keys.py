import traceback

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QHeaderView, QFileDialog, QMessageBox, QTableWidgetItem

from exceptions import PrivateKeyDecryptionError
from gui.utils import open_child, lambda_w_capture, back
from gui.password_prompt import UI_PasswordPrompt
from gui.generate_key import UI_GenerateKey
from ring import PrivateRing, import_private_entry, load_key_info


def fetch_entries() -> list:
    return [[entry.user, entry.public_key.get_key_ID()] for entry in PrivateRing.get_all()]


class UI_PrivateKeys(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent: QMainWindow = parent
        self.setupUi()
        self.refresh()
        self.passphrase = None

    def setupUi(self):
        self.setWindowTitle('Private Keys')
        self.resize(880, 524)
        self.centralwidget = QtWidgets.QWidget(self)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 820, 441))

        self.tableWidget.setColumnCount(5)

        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("User"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Key ID"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem(""))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem(""))
        self.tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem(""))

        self.generate_key_button = QtWidgets.QPushButton('Generate Key', self.centralwidget)
        self.generate_key_button.setGeometry(QtCore.QRect(240, 470, 181, 41))
        self.generate_key_button.clicked.connect(lambda: open_child(self, UI_GenerateKey()))

        self.back_button = QtWidgets.QPushButton('Back', self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(10, 470, 100, 41))
        self.back_button.clicked.connect(lambda: back(self))

        def import_private_key():
            files = QFileDialog.getOpenFileNames(self, 'Choose Private Keys')
            for file in files[0]:
                def save_passphrase(x):
                    self.passphrase = bytes(x, 'utf-8')
                    return True

                try:
                    user, is_private, algorithm, keys = load_key_info(file)
                    p = UI_PasswordPrompt(self, user + " [" + keys[1].get_key_ID().hex() + "]", lambda x: save_passphrase(x))
                    p.exec_()

                    if not self.passphrase:
                        return

                    import_private_entry(user, is_private, algorithm, keys, self.passphrase)
                    self.refresh()

                except Exception as e:
                    traceback.print_exc()
                    QMessageBox.information(self, 'Error', str(e), QMessageBox.Ok)

        self.import_key_button = QtWidgets.QPushButton('Import Keys', self.centralwidget)
        self.import_key_button.setGeometry(QtCore.QRect(450, 470, 181, 41))
        self.import_key_button.clicked.connect(import_private_key)

        self.setCentralWidget(self.centralwidget)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        for i in range(5):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)

    def refresh(self):
        entries = fetch_entries()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(entries))

        def delete_entry(key_ID: bytes):
            PrivateRing.remove(key_ID)
            self.refresh()

        def export_public_key(key_ID: bytes):
            file = QFileDialog.getSaveFileName(self, 'Save Public Key')
            if file and file[0] != '':
                PrivateRing.get_by_key_ID(key_ID).export_public(file[0] + '.pem')

        def export_private_key(key_ID: bytes):
            entry = PrivateRing.get_by_key_ID(key_ID)
            print(entry.user)

            def f(passphrase):
                try:
                    PrivateRing.get_by_key_ID(key_ID).get_private_key(bytes(passphrase, 'utf-8'))
                    self.passphrase = bytes(passphrase, 'utf-8')
                    return True
                except PrivateKeyDecryptionError:
                    self.passphrase = None
                    QMessageBox.information(self, 'Wrong passphrase', "You entered a wrong passphrase", QMessageBox.Ok)
                    return False

            p = UI_PasswordPrompt(self, entry.user + "[" + entry.public_key.get_key_ID().hex() + "]", lambda x: f(x))
            p.exec_()

            if not self.passphrase:
                return

            file = QFileDialog.getSaveFileName(self, 'Save Private Key')
            if file[0] != '':
                print(self.passphrase)
                PrivateRing.get_by_key_ID(key_ID).export(file[0] + '.pem', self.passphrase)

        for idx, e in enumerate(entries):
            self.tableWidget.setItem(idx, 0, QTableWidgetItem(e[0]))
            self.tableWidget.setItem(idx, 1, QTableWidgetItem(e[1].hex()))

            btn = QPushButton('delete', self.tableWidget)
            btn.clicked.connect(lambda_w_capture(delete_entry, e[1]))
            self.tableWidget.setCellWidget(idx, 2, btn)

            btn = QPushButton('export private', self.tableWidget)
            btn.clicked.connect(lambda_w_capture(export_private_key, e[1]))
            self.tableWidget.setCellWidget(idx, 3, btn)

            btn = QPushButton('export public', self.tableWidget)
            btn.clicked.connect(lambda_w_capture(export_public_key, e[1]))
            self.tableWidget.setCellWidget(idx, 4, btn)
