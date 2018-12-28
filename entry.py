import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
from queue import Queue

import DB_manager
from utils import SimpleHandler, DBHandler


class Entry(QtWidgets.QWidget):
    """docstring for App"""

    def __init__(self, database, id_table_name, visit_table_name, qu=None):
        super(Entry, self).__init__()
        uic.loadUi('entry.ui', self)
        self.setWindowTitle('APP Pyqt Gui')
        self.setLayout(self.verticalLayout_3)
        self.dbu = database
        self.identityTable = id_table_name
        self.visitTable = visit_table_name
        self.qu = qu

        self.total_visits = self.dbu.GetTotalVisits(self.visitTable)[0][0]
        self.inputs = {'fname': self.fnameLineEdit,
                       'mname': self.mnameLineEdit,
                       'lname': self.lnameLineEdit,
                       'sex': self.sexComboBox,
                       'age': self.ageSpinBox
                       }

        self.patient_id = None
        self.full_list_present = True

        self.submitPushButton.setEnabled(False)
        self.inputs['sex'].addItems(['Select', 'M', 'F'])

        self.clearPushButton.clicked.connect(self.reset_age)
        self.clearPushButton.clicked.connect(self.reset_sex)
        self.submitPushButton.clicked.connect(self.submit)
        self.treeWidget.itemClicked.connect(self.save_for_queue)
        self.addPushButton.clicked.connect(self.add_to_queue)

        self.inputs['fname'].textChanged.connect(self.query)
        self.inputs['mname'].textChanged.connect(self.query)
        self.inputs['lname'].textChanged.connect(self.query)
        self.inputs['sex'].currentIndexChanged.connect(self.query)
        self.inputs['age'].valueChanged.connect(self.query)

        job = DBHandler(fn1=self.dbu.GetColumns, fn2=self.dbu.GetTable, tableName=self.identityTable)
        job.signals.result.connect(self.update_tree)
        job.signals.finished.connect(self.enableSubmitButton)
        self.qu.put(job)

    @pyqtSlot()
    def reset_age(self):
        self.inputs['age'].setValue(0)

    @pyqtSlot()
    def reset_sex(self):
        self.inputs['sex'].setCurrentIndex(0)

    @pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def save_for_queue(self, item, col):
        self.patient_id = item.text(0)

    @pyqtSlot()
    def add_to_queue(self):
        self.total_visits += 1
        job = SimpleHandler(self.dbu.AddToQueue, self.visitTable, self.patient_id, self.total_visits)
        self.qu.put(job)

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
            job2 = DBHandler(fn1=self.dbu.GetColumns, fn2=self.dbu.Query, tableName=self.identityTable, data=query_data)
            job2.signals.result.connect(self.update_tree)
            self.qu.put(job2)
            self.full_list_present = False
        elif not self.full_list_present:
            job = DBHandler(fn1=self.dbu.GetColumns, fn2=self.dbu.GetTable, tableName=self.identityTable)
            job.signals.result.connect(self.update_tree)
            self.qu.put(job)
            self.full_list_present = True

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
        job = SimpleHandler(self.dbu.AddRecordToTable, self.identityTable, (fname, mname, lname, sex, age))
        self.qu.put(job)
        query_data = {'first_name': fname, 'middle_name': mname, 'last_name': lname, 'sex': sex, 'age': str(age)}
        job2 = DBHandler(fn1=self.dbu.GetColumns, fn2=self.dbu.Query, tableName=self.identityTable, data=query_data)
        job2.signals.finished.connect(self.enableSubmitButton)
        job2.signals.result.connect(self.update_tree)
        self.qu.put(job2)
        self.full_list_present = False

    @pyqtSlot(list)
    def update_tree(self, data):
        col, table = data
        for c in range(len(col)):
            self.treeWidget.headerItem().setText(c, col[c][0])

        self.treeWidget.clear()

        for item in range(len(table)):
            QtWidgets.QTreeWidgetItem(self.treeWidget)
            for value in range(len(table[item])):
                self.treeWidget.topLevelItem(item).setText(value, str(table[item][value]))


if __name__ == '__main__':

    db = 'patient_try'
    identityTable = 'patient'
    visitTable = 'visits'
    dbu = DB_manager.DatabaseUtility(db)
    app = QtWidgets.QApplication(sys.argv)
    widget = Entry(dbu, identityTable, visitTable, Queue())
    widget.show()
    app.exec_()
    dbu.__del__()
    app.exit()
