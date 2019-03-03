from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot

from utils import SimpleHandler


class Katar(QtWidgets.QWidget):

    def __init__(self, app=None, dbu=None, id_table=None, visit_table=None, qu=None):
        super(Katar, self).__init__()
        self.app = app
        self.dbu = dbu
        self.id_table = id_table
        self.visit_table = visit_table
        self.qu = qu
        self.app.setLayout(self.app.verticalLayout)
        self.app.refreshPushButton.clicked.connect(self.update_queue)
        self.update_queue()

    @pyqtSlot(list)
    def update_tree(self, table):
        col = [['SNo'], ['Name'], ['P_id']]

        for c in range(len(col)):
            self.app.queueTreeWidget.headerItem().setText(c, col[c][0])

        self.app.queueTreeWidget.clear()

        for item in range(len(table)):
            QtWidgets.QTreeWidgetItem(self.app.queueTreeWidget)
            for value in range(len(table[item])):
                self.app.queueTreeWidget.topLevelItem(item).setText(value, str(table[item][value]))

    @pyqtSlot()
    def update_queue(self):
        job = SimpleHandler(self.dbu.FetchQueue, self.id_table, self.visit_table)
        job.signals.result.connect(self.update_tree)
        self.qu.put(job)


if __name__ == '__main__':
    pass