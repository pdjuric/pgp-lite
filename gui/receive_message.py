from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from decryption import DecryptMessage
from message import Message


class UI_ReceiveMessage(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setupUi(self)

    def show(self) -> None:
        file = QFileDialog.getOpenFileName(self, 'Save Message')
        if file:
            with open(file[0], 'rb') as file:
                msg = file.read()
                message = Message("")
                message.append(msg)
                DecryptMessage().exec(message)
        super().show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("ReceiveMessage")
        MainWindow.resize(549, 443)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.log_list = QtWidgets.QListWidget(self.centralwidget)
        self.log_list.setGeometry(QtCore.QRect(20, 20, 511, 371))
        self.log_list.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.log_list.setObjectName("log")

        self.save_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_button.setGeometry(QtCore.QRect(160, 400, 113, 32))
        self.save_button.setObjectName("save button")
        self.save_button.clicked.connect(self.save_message)

        self.ok_button = QtWidgets.QPushButton(self.centralwidget)
        self.ok_button.setGeometry(QtCore.QRect(280, 400, 113, 32))
        self.ok_button.setObjectName("ok button")
        self.ok_button.clicked.connect(self.return_to_main_menu)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def return_to_main_menu(self):
        self.parent.show()
        self.hide()

    def save_message(self):
        file = QFileDialog.getSaveFileName(self, 'Save Message')
        if file and file[0] != "":
            with open(file[0] + '.txt', 'w') as file:
                last_item = self.log_list.item(self.log_list.count() - 1).text()
                text = last_item[last_item.rfind("- ") + 20:]
                file.write(text)
        self.return_to_main_menu()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Receive a Message"))
        __sortingEnabled = self.log_list.isSortingEnabled()
        self.log_list.setSortingEnabled(False)
        self.log_list.setSortingEnabled(__sortingEnabled)
        self.save_button.setText(_translate("MainWindow", "Save"))
        self.ok_button.setText(_translate("MainWindow", "OK"))
