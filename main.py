import sys
from Qt import QtCore, QtWidgets, QtCompat


class App(QtWidgets.QDialog):
    """docstring for Life3Coding"""
    def __init__(self):
        super().__init__()
        QtCompat.loadUi('app2.ui', self)
        self.setWindowTitle('APP Pyqt Gui')
        # self.pushButton.clicked.connect(self.on_pushButton_clicked)

    # def on_pushButton_clicked(self):
    #     self.label_2.setText('Welcome: ' + self.lineEdit.text())


app = QtWidgets.QApplication(sys.argv)
widget = App()
widget.show()
sys.exit(app.exec_())
