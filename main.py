import sys

from PyQt5.QtWidgets import QApplication

from gui.main_window import UI_PGPlite

app = QApplication(sys.argv)
win = UI_PGPlite()
win.show()
sys.exit(app.exec())
