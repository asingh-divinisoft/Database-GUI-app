import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QThread
from queue import Queue

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

        self.full_list_present = True

        self.submitPushButton.setEnabled(False)
        self.inputs['sex'].addItems(['Select', 'M', 'F'])

        self.clearPushButton.clicked.connect(self.reset_age)
        self.clearPushButton.clicked.connect(self.reset_sex)
        self.submitPushButton.clicked.connect(self.submit)
        self.treeWidget.itemClicked.connect(self.printin)

        self.inputs['fname'].textChanged.connect(self.query)
        self.inputs['mname'].textChanged.connect(self.query)
        self.inputs['lname'].textChanged.connect(self.query)
        self.inputs['sex'].currentIndexChanged.connect(self.query)
        self.inputs['age'].valueChanged.connect(self.query)

        job = DBHandler(fn1=self.dbu.GetColumns, fn2=self.dbu.GetTable, tableName=self.tableName)
        job.signals.result.connect(self.update_tree)
        job.signals.finished.connect(self.enableSubmitButton)

        self.qu = Queue()
        worker = Worker(qu=self.qu, parent=self)

        self.qu.put(job)
        worker.start()

    @pyqtSlot()
    def reset_age(self):
        self.inputs['age'].setValue(0)

    @pyqtSlot()
    def reset_sex(self):
        self.inputs['sex'].setCurrentIndex(0)

    @pyqtSlot()
    def query(self):
        input_data = {}
        query_data = {}

        input_data['first_name'] = self.inputs['fname'].text()
        input_data['middle_name'] = self.inputs['mname'].text()
        input_data['last_name'] = self.inputs['lname'].text()
        input_data['sex'] = self.inputs['sex'].currentText()
        input_data['age'] = str(self.inputs['age'].value())

        if input_data['first_name'] != '':
            query_data['first_name'] = input_data['first_name']

        if input_data['middle_name'] != '':
            query_data['middle_name'] = input_data['middle_name']

        if input_data['last_name'] != '':
            query_data['last_name'] = input_data['last_name']

        if input_data['sex'] != 'Select':
            query_data['sex'] = input_data['sex']

        if input_data['age'] != '0':
            query_data['age'] = input_data['age']

        if len(query_data) > 0:
            job2 = DBHandler(fn1=self.dbu.GetColumns, fn2=self.dbu.Query, tableName=self.tableName)
            job2.signals.result.connect(self.update_tree)
            self.sig.connect(job2.take_input)
            self.sig.emit(query_data)
            self.qu.put(job2)
            self.full_list_present = False
        elif not self.full_list_present:
            job = DBHandler(fn1=self.dbu.GetColumns, fn2=self.dbu.GetTable, tableName=self.tableName)
            job.signals.result.connect(self.update_tree)
            self.qu.put(job)
            self.full_list_present = True

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
    def submit(self):
        self.submitPushButton.setEnabled(False)
        fname = self.inputs['fname'].text()
        mname = self.inputs['mname'].text()
        lname = self.inputs['lname'].text()
        sex = self.inputs['sex'].currentText()
        age = self.inputs['age'].value()
        self.dbu.AddRecordToTable(self.tableName, (fname, mname, lname, sex, age))
        job = DBHandler(fn1=self.dbu.GetColumns, fn2=self.dbu.GetTable, tableName=self.tableName)
        job.signals.result.connect(self.update_tree)
        job.signals.finished.connect(self.enableSubmitButton)
        self.qu.put(job)

    @pyqtSlot(list, list)
    def update_tree(self, col, table):

        for c in range(len(col)):
            self.treeWidget.headerItem().setText(c, col[c][0])

        self.treeWidget.clear()

        for item in range(len(table)):
            QtWidgets.QTreeWidgetItem(self.treeWidget)
            for value in range(len(table[item])):
                self.treeWidget.topLevelItem(item).setText(value, str(table[item][value]))


class WorkerSignals(QObject):
    result = pyqtSignal(list, list)
    finished = pyqtSignal()


class DBHandler:
    """
    Just a regular class that emits signals
    """
    def __init__(self, fn1=None, fn2=None, tableName=None):
        self.signals = WorkerSignals()
        self.tableName = tableName
        self.fn1 = fn1
        self.fn2 = fn2
        self.data = None

    def take_input(self, data):
        self.data = data

    def run(self):
        col = self.fn1(self.tableName)
        table = self.fn2(self.tableName, self.data)
        self.signals.finished.emit()
        self.signals.result.emit(col, table)


class Worker(QThread):
    def __init__(self, qu, parent=None):
        super(Worker, self).__init__(parent=parent)
        self.in_qu = qu
        self.running = True

    def run(self):
        while self.running:  # to keep the thread running
            if not self.in_qu.empty():
                job = self.in_qu.get()
                job.run()
            else:
                pass


if __name__ == '__main__':

    db = 'patient_try'
    tableName = 'patient'
    dbu = DB_manager.DatabaseUtility(db)
    app = QtWidgets.QApplication(sys.argv)
    widget = App(dbu, tableName)
    widget.show()
    sys.exit(app.exec_())
