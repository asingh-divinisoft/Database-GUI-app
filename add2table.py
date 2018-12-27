import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot

import DB_manager


class App(QtWidgets.QDialog):
    """docstring for App"""

    def __init__(self, database, tableName):
        super().__init__()
        self.tableName = tableName
        uic.loadUi('simple_db_form.ui', self)
        self.setWindowTitle('APP Pyqt Gui')
        self.dbu = DB_manager.DatabaseUtility(database=database)
        self.pushButton.clicked.connect(self.Commit)
        self.worke = DB_handler(db=self.dbu, tableName=self.tableName)
        self.worke.sig1.connect(self.UpdateTree)
        self.worke.start()

    @pyqtSlot()
    def Commit(self):
        text = self.lineEdit.text()
        self.lineEdit.setText('')
        self.dbu.AddEntryToTable(text)
        self.worke.start()

    @pyqtSlot(list, list)
    def UpdateTree(self, col, table):

        for c in range(len(col)):
            self.treeWidget.headerItem().setText(c, col[c][0])

        self.treeWidget.clear()

        for item in range(len(table)):
            QtWidgets.QTreeWidgetItem(self.treeWidget)
            for value in range(len(table[item])):
                self.treeWidget.topLevelItem(item).setText(value, str(table[item][value]))


class DB_handler(QThread):
    sig1 = pyqtSignal(list, list)

    def __init__(self, parent=None, db=None, tableName=None):
        super(DB_handler, self).__init__(parent)
        self.db = db
        self.tableName = tableName

    def run(self):
        col = self.db.GetColumns(self.tableName)
        table = self.db.GetTable(self.tableName)
        self.sig1.emit(col, table)


if __name__ == '__main__':

    db = 'myFirstDB'
    tableName = 'test8'
    app = QtWidgets.QApplication(sys.argv)
    widget = App(db, tableName)
    widget.show()
    app.exec_()
    app.exit()
