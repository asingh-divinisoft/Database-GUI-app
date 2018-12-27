import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot

import entry
import DB_manager


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.db = 'patient_try'
        self.identityTable = 'patient'
        self.visitTable = 'visits'
        self.dbu = DB_manager.DatabaseUtility(self.db)

        self.queueWidget = QtWidgets.QTreeWidget()

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.queueWidget)
        layout.addWidget(entry.App(self.dbu, self.identityTable, self.visitTable))

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    @pyqtSlot(list, list)
    def update_tree(self, col, table):

        for c in range(len(col)):
            self.queueWidget.headerItem().setText(c, col[c][0])

        self.queueWidget.clear()

        for item in range(len(table)):
            QtWidgets.QTreeWidgetItem(self.queueWidget)
            for value in range(len(table[item])):
                self.queueWidget.topLevelItem(item).setText(value, str(table[item][value]))

    def update_queue(self):
        job = entry.SimpleHandler(self.dbu, self.identityTable, self.visitTable)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
    app.exit()

