import sys
from Qt import QtCore, QtWidgets, QtCompat
import DB_manager

class App(QtWidgets.QDialog):
    """docstring for Life3Coding"""
    def __init__(self, database, tableName):
        super().__init__()
        QtCompat.loadUi('simple_db_form.ui', self)
        self.setWindowTitle('APP Pyqt Gui')
        self.dbu = DB_manager.DatabaseUtility(database=database, tableName=tableName)
        self.pushButton.clicked.connect(self.Commit)
        self.UpdateTree()

    def Commit(self):
        text = self.lineEdit.text()
        self.dbu.AddEntryToTable(text)
        self.UpdateTree()

    def UpdateTree(self):
        col = self.dbu.GetColumns()
        table = self.dbu.GetTable()

        for c in range(len(col)):
            self.treeWidget.headerItem().setText(c, col[c][0])

        self.treeWidget.clear()

        for item in range(len(table)):
            QtWidgets.QTreeWidgetItem(self.treeWidget)
            for value in range(len(table[item])):
                self.treeWidget.topLevelItem(item).setText(value, str(table[item][value]))


if __name__ == '__main__':

    db = 'myFirstDB'
    tableName = 'test8'
    app = QtWidgets.QApplication(sys.argv)
    widget = App(db, tableName)
    widget.show()
    sys.exit(app.exec_())
