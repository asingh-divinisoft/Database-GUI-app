import sys
from queue import Queue

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot

import DB_manager
from utils import SimpleHandler


class Katar(QtWidgets.QWidget):

    def __init__(self, dbu=None, id_table=None, visit_table=None, qu=None):
        super(Katar, self).__init__()
        uic.loadUi('katar.ui', self)
        self.dbu = dbu
        self.id_table = id_table
        self.visit_table = visit_table
        self.qu = qu
        self.setLayout(self.verticalLayout)
        self.refreshPushButton.clicked.connect(self.update_queue)
        self.update_queue()

    @pyqtSlot(list)
    def update_tree(self, table):
        col = [['SNo'], ['Name'], ['P_id']]

        for c in range(len(col)):
            self.queueWidget.headerItem().setText(c, col[c][0])

        self.queueWidget.clear()

        for item in range(len(table)):
            QtWidgets.QTreeWidgetItem(self.queueWidget)
            for value in range(len(table[item])):
                self.queueWidget.topLevelItem(item).setText(value, str(table[item][value]))

    @pyqtSlot()
    def update_queue(self):
        job = SimpleHandler(self.dbu.FetchQueue, self.id_table, self.visit_table)
        job.signals.result.connect(self.update_tree)
        self.qu.put(job)


if __name__ == '__main__':
    db = 'patient_try'
    identityTable = 'patient'
    visitTable = 'visits'
    dbu = DB_manager.DatabaseUtility(db)
    app = QtWidgets.QApplication(sys.argv)
    widget = Katar(dbu, identityTable, visitTable, Queue())
    widget.show()
    app.exec_()
    dbu.__del__()
    app.exit()