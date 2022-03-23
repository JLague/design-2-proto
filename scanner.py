import multiprocessing as mp
from multiprocessing.connection import Connection
from PySide6.QtCore import QObject, Signal, QThread, QRunnable
from threading import Thread
import comm

class ScannerWrapper(QObject):
    code_scanned = Signal(str)
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.scanner = Scanner(self.code_scanned)

class Scanner(QThread):
    code_scanned = Signal(str)
    def __init__(self, pipe: Connection, parent=None) -> None:
        QThread.__init__(self)
        # QObject.__init__(self, parent)
        # mp.Process.__init__(self)
        # QThread.__init__(self)
        # Thread.__init__(self)
        self.pipe = pipe
        # self.code_scanned = Signal(str)

    def run(self):
        with comm.ArduinoComm() as ard_comm:
            comm.wait_until(ard_comm, comm.SWEEP_END)
            while True:
                code = comm.find_barcode(ard_comm)
                if code:
                    self.pipe.send(code)
                    self.code_scanned.emit(code)
                    # print(code)