from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QMainWindow

from ring import PublicRing, User


def fetch_entries(key_ID):
    public_ring_entry = PublicRing.get_by_key_ID(key_ID)
    return [[user.ID, str(user.trust)] for user in User.all_users.values()
            if user not in public_ring_entry.get_signatures() and
            user != public_ring_entry.user]


class UI_AddSignature(QDialog):

    def __init__(self, parent, key_ID):
        super().__init__(parent)
        self.parent: QMainWindow = parent
        self.key_ID = key_ID
        self.setupUi(self, fetch_entries(key_ID))

    def setupUi(self, Dialog, data):
        self.setWindowTitle('Add Signature')
        Dialog.resize(341, 261)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(90, 220, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)

        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(20, 20, 301, 192))
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.listWidget.setSelectionRectVisible(True)

        for user, trust in data:
            item = QtWidgets.QListWidgetItem()
            item.setText(user + ' ' + str(trust))
            self.listWidget.addItem(item)

        def add_signature():
            for item in self.listWidget.selectedItems():
                text = item.text()
                text = text[:text.rfind('>') + 1]
                PublicRing.get_by_key_ID(self.key_ID).add_signature(User.get(text))
            self.parent.refresh()
            self.hide()

        self.buttonBox.accepted.connect(add_signature)
        self.buttonBox.rejected.connect(lambda: self.hide())
