from PyQt5.QtCore import QObject, pyqtSignal, QThread


class WorkerSignals(QObject):
    result = pyqtSignal(list)
    finished = pyqtSignal()


class SimpleHandler:

    def __init__(self, fn, *args, **kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        result = self.fn(*self.args, **self.kwargs)
        self.signals.finished.emit()
        if result is None:
            result = []
        self.signals.result.emit(result)


class DBHandler:
    """
    Just a regular class that emits signals
    """
    def __init__(self, fn1=None, fn2=None, tableName=None, data=None):
        self.signals = WorkerSignals()
        self.tableName = tableName
        self.fn1 = fn1
        self.fn2 = fn2
        self.data = data

    def run(self):
        col = self.fn1(self.tableName)
        table = self.fn2(self.tableName, self.data)
        self.signals.finished.emit()
        self.signals.result.emit([col, table])


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