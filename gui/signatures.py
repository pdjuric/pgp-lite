from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QMainWindow, QTableWidgetItem, QTableWidget, QPushButton, QAbstractItemView

from gui.add_signature import UI_AddSignature
from ring import PublicRing


def fetch_entries(key_ID):
    return [[user.ID, user.trust] for user in PublicRing.get_by_key_ID(key_ID).get_signatures()]


class UI_Signatures(QDialog):

    def __init__(self, parent, key_ID):
        super().__init__(parent)
        self.parent: QMainWindow = parent
        self.key_ID = key_ID
        self.setupUi()
        self.refresh()

    def setupUi(self):
        self.setWindowTitle('Signatures')
        self.resize(340, 450)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 300, 400))

        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem('User'))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem('Trust'))

        self.add_signature_button = QPushButton('Add Signature', self)
        self.add_signature_button.setGeometry(QtCore.QRect(50, 420, 113, 32))
        self.add_signature_button.clicked.connect(lambda: UI_AddSignature(self, self.key_ID).show())

        def update_legitimacies():
            self.parent.recalculate_legitimacies()
            self.hide()

        self.ok_button = QPushButton('OK', self)
        self.ok_button.setGeometry(QtCore.QRect(180, 420, 113, 32))
        self.ok_button.clicked.connect(update_legitimacies)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)

    def refresh(self):
        entries = fetch_entries(self.key_ID)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(entries))

        for idx, e in enumerate(entries):
            self.tableWidget.setItem(idx, 0, QTableWidgetItem(e[0]))
            self.tableWidget.setItem(idx, 1, QTableWidgetItem(str(e[1])))

