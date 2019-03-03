import sys
from queue import Queue

from PyQt5 import QtWidgets, uic
import entry
import katar
import DB_manager
from utils import Worker


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('material.ui', self)

        self.db = 'patient_try'
        self.identityTable = 'patient'
        self.visitTable = 'visits'
        self.dbu = DB_manager.DatabaseUtility(self.db)
        self.qu = Queue()
        self.worker = Worker(qu=self.qu, parent=self)
        self.entry_app = entry.Entry(self, self.dbu, self.identityTable, self.visitTable, self.qu)
        self.katar_app = katar.Katar(self, self.dbu, self.identityTable, self.visitTable, self.qu)
        self.addPushButton.clicked.connect(self.katar_app.update_queue)

        self.worker.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
    app.exit()
