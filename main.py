import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QSizePolicy

import entry
import DB_manager


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.db = 'patient_try'
        self.tableName = 'patient'
        self.dbu = DB_manager.DatabaseUtility(self.db)

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.button = QtWidgets.QPushButton("Next")
        self.button2 = QtWidgets.QPushButton("Back")

        self.button.clicked.connect(self.__next_page)
        self.button2.clicked.connect(self.__previous_page)

        btn_widget = QtWidgets.QWidget()
        layout2 = QtWidgets.QHBoxLayout()
        spacerItem = QtWidgets.QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout2.addItem(spacerItem)
        layout2.addWidget(self.button2)
        layout2.addWidget(self.button)
        btn_widget.setLayout(layout2)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        layout.addWidget(btn_widget)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.stacked_widget.addWidget(entry.App(self.dbu, self.tableName))
        self.stacked_widget.addWidget(QtWidgets.QLabel("Page 1"))
        self.stacked_widget.addWidget(QtWidgets.QLabel("Page 2"))
        self.stacked_widget.addWidget(QtWidgets.QLabel("Page 3"))

    def __next_page(self):
        idx = self.stacked_widget.currentIndex()
        if idx < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(idx + 1)
        else:
            self.stacked_widget.setCurrentIndex(0)

    def __previous_page(self):
        idx = self.stacked_widget.currentIndex()
        if idx > 0:
            self.stacked_widget.setCurrentIndex(idx - 1)
        else:
            self.stacked_widget.setCurrentIndex(self.stacked_widget.count() - 1)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

