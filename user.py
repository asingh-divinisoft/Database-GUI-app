import sys
from queue import Queue

from PyQt5 import QtWidgets
from PyQt5.QtCore import QLine
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSizePolicy, QFrame

import entry
import katar
import DB_manager
from utils import Worker


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.db = 'patient_try'
        self.identityTable = 'patient'
        self.visitTable = 'visits'
        self.dbu = DB_manager.DatabaseUtility(self.db)
        self.qu = Queue()
        self.worker = Worker(qu=self.qu, parent=self)
        self.katar_app = katar.Katar(self.dbu, self.identityTable, self.visitTable, self.qu)
        self.entry_app = entry.Entry(self.dbu, self.identityTable, self.visitTable, self.qu)
        self.entry_app.addPushButton.clicked.connect(self.katar_app.update_queue)
        self.katar_app.refreshPushButton.clicked.connect(self.katar_app.update_queue)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.katar_app)
        line = QFrame()
        line.setFrameShadow(QFrame.Sunken)
        line.setFrameShape(QFrame.VLine)
        layout.addWidget(line)
        layout.addWidget(self.entry_app)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.worker.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
    app.exit()

