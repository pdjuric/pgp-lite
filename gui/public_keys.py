import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QHeaderView, QPushButton, QTableWidgetItem
import traceback

from gui.utils import open_child, back, lambda_show, lambda_w_capture
from gui.public_key_imported_alert import UI_PublicKeyImportedAlert
from gui.signatures import UI_Signatures
from ring import PublicRing, import_public_entry, load_key_info, User
from ring.public import Trust


def fetch_entries() -> list:
    return [[entry.user.ID, entry.public_key.get_key_ID(), entry.user.trust, entry.get_key_legitimacy()] for entry in
            PublicRing.get_all()]


class UI_PublicKeys(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent: QMainWindow = parent
        self.setupUi()
        self.refresh()

    def setupUi(self):
        self.setWindowTitle('Public Keys')
        self.resize(880, 524)
        self.centralwidget = QtWidgets.QWidget(self)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 820, 441))

        self.tableWidget.setColumnCount(7)

        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("User"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Key ID"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Owner trust"))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Key legitimacy"))
        self.tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem(""))
        self.tableWidget.setHorizontalHeaderItem(5, QTableWidgetItem(""))
        self.tableWidget.setHorizontalHeaderItem(6, QTableWidgetItem(""))

        self.back_button = QtWidgets.QPushButton("Back", self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(10, 470, 100, 41))
        self.back_button.clicked.connect(lambda: back(self))

        def import_public_key():
            files = QFileDialog.getOpenFileNames(self, 'Choose Public Keys')
            for file in files[0]:
                def callback(name: str):
                    user = User.get(name)

                    def set_trust(trust: Trust):
                        user.trust = trust
                        self.refresh()

                    return set_trust

                try:
                    user, is_private, algorithm, keys = load_key_info(file)
                    user = User.get(user)
                    UI_PublicKeyImportedAlert(self, user.ID, keys[1].get_key_ID(), user.trust, callback(user.ID)).show()
                    import_public_entry(user, is_private, algorithm, keys)
                    self.refresh()

                except Exception as e:
                    traceback.print_exc()
                    QMessageBox.information(self, 'Error', str(e), QMessageBox.Ok)

        self.import_key_button = QtWidgets.QPushButton("Import Keys", self.centralwidget)
        self.import_key_button.setGeometry(QtCore.QRect(290, 470, 181, 41))
        self.import_key_button.clicked.connect(import_public_key)

        self.setCentralWidget(self.centralwidget)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.tableWidget.setSortingEnabled(False)
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
            PublicRing.remove(key_ID)
            self.refresh()

        def export_key(key_ID: bytes):
            file = QFileDialog.getSaveFileName(self, 'Save Public Key')
            if file and file[0] != '':
                PublicRing.get_by_key_ID(key_ID).export(file[0] + '.pem')

        for idx, e in enumerate(entries):
            self.tableWidget.setItem(idx, 0, QTableWidgetItem(e[0]))
            self.tableWidget.setItem(idx, 1, QTableWidgetItem(e[1].hex()))
            self.tableWidget.setItem(idx, 2, QTableWidgetItem(str(e[2])))
            self.tableWidget.setItem(idx, 3, QTableWidgetItem('legitimate' if e[3] else 'not legitimate'))

            btn = QPushButton('delete', self.tableWidget)
            btn.clicked.connect(lambda_w_capture(delete_entry, e[1]))
            self.tableWidget.setCellWidget(idx, 4, btn)

            btn = QPushButton('export', self.tableWidget)
            btn.clicked.connect(lambda_w_capture(export_key, e[1]))
            self.tableWidget.setCellWidget(idx, 5, btn)

            btn = QPushButton('signatures', self.tableWidget)
            btn.clicked.connect(lambda_show(UI_Signatures(self, e[1])))
            self.tableWidget.setCellWidget(idx, 6, btn)

    def recalculate_legitimacies(self):
        entries = fetch_entries()
        for idx, e in enumerate(entries):
            self.tableWidget.item(idx, 3).setText('legitimate' if e[3] else 'not legitimate')
