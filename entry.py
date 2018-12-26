import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThreadPool, QRunnable, QObject

import DB_manager


class App(QtWidgets.QWidget):
    """docstring for App"""
    sig = pyqtSignal(dict)

    def __init__(self, database, tableName):
        super(App, self).__init__()
        uic.loadUi('entry.ui', self)
        self.setWindowTitle('APP Pyqt Gui')
        self.dbu = database
        self.tableName = tableName

        self.inputs = {'fname': self.fnameLineEdit,
                       'mname': self.mnameLineEdit,
                       'lname': self.lnameLineEdit,
                       'sex': self.sexComboBox,
                       'age': self.ageSpinBox
                       }

        self.inputs['sex'].addItems(['M', 'F'])
        self.inputs['fname'].editingFinished.connect(self.fname_query)
        self.submitPushButton.clicked.connect(self.Commit)
        self.treeWidget.itemClicked.connect(self.printin)

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        worker = DB_handler(fn1=self.dbu.GetColumns, fn2=self.dbu.GetTable, tableName=self.tableName)
        worker.signals.result.connect(self.UpdateTree)
        worker.signals.finished.connect(self.enableSubmitButton)

        self.submitPushButton.setEnabled(False)
        self.threadpool.start(worker)

        self.input_data = {}

    @pyqtSlot()
    def fname_query(self):
        self.input_data['first_name'] = self.inputs['fname'].text()
        if self.input_data['first_name'] is '':
            return
        worker2 = DB_handler(fn1=self.dbu.GetColumns, fn2=self.dbu.Query, tableName=self.tableName)
        worker2.signals.result.connect(self.UpdateTree)
        self.sig.connect(worker2.take_input)
        self.sig.emit(self.input_data)
        self.threadpool.start(worker2)

    @pyqtSlot()
    def selectionchange(self):
        # print(self.inputs['sex'].currentText())
        pass

    @pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def printin(self, item, col):
        print(item.text(0))

    @pyqtSlot()
    def enableSubmitButton(self):
        self.submitPushButton.setEnabled(True)

    @pyqtSlot()
    def Commit(self):
        self.submitPushButton.setEnabled(False)
        fname = self.inputs['fname'].text()
        mname = self.inputs['mname'].text()
        lname = self.inputs['lname'].text()
        sex = self.inputs['sex'].currentText()
        age = self.inputs['age'].value()
        self.dbu.AddRecordToTable(self.tableName, (fname, mname, lname, sex, age))
        worker = DB_handler(fn1=self.dbu.GetColumns, fn2=self.dbu.GetTable, tableName=self.tableName)
        worker.signals.result.connect(self.UpdateTree)
        worker.signals.finished.connect(self.enableSubmitButton)
        self.threadpool.start(worker)

    @pyqtSlot(list, list)
    def UpdateTree(self, col, table):

        for c in range(len(col)):
            self.treeWidget.headerItem().setText(c, col[c][0])

        self.treeWidget.clear()

        for item in range(len(table)):
            QtWidgets.QTreeWidgetItem(self.treeWidget)
            for value in range(len(table[item])):
                self.treeWidget.topLevelItem(item).setText(value, str(table[item][value]))


class DB_handler(QRunnable):

    def __init__(self, fn1=None, fn2=None, tableName=None):
        super(DB_handler, self).__init__()
        self.signals = WorkerSignals()
        self.tableName = tableName
        self.fn1 = fn1
        self.fn2 = fn2
        self.data = None

    def take_input(self, data):
        self.data = data

    @pyqtSlot()
    def run(self):
        col = self.fn1(self.tableName)
        table = self.fn2(self.tableName, self.data)
        self.signals.finished.emit()
        self.signals.result.emit(col, table)


class WorkerSignals(QObject):
    result = pyqtSignal(list, list)
    finished = pyqtSignal()


if __name__ == '__main__':

    db = 'patient_try'
    tableName = 'patient'
    dbu = DB_manager.DatabaseUtility(db)
    app = QtWidgets.QApplication(sys.argv)
    widget = App(dbu, tableName)
    widget.show()
    sys.exit(app.exec_())
