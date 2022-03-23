import multiprocessing as mp
from PySide6.QtCore import Signal, QThread
import comm

class Scanner(QThread):
    code_scanned = Signal(str)
    def __init__(self, parent=None) -> None:
        QThread.__init__(self, parent)
        self.is_running = False

    def scan_test(self):
        counter = 0
        while self.is_running and counter < 3:
            code = comm.find_barcode_test()
            if code: self.code_scanned.emit(code.decode('utf-8'))
            counter += 1

    def scan(self):
        with comm.ArduinoComm() as ard_comm:
            while self.is_running:
                code = comm.find_barcode(ard_comm)
                if code: self.code_scanned.emit(code.decode('utf-8'))

    def run(self):
        self.is_running = True
        self.scan()
        # self.scan_test()

    def stop(self):
        self.is_running = False
        self.wait()
