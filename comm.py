import time
import serial
import struct
from barcode import Barcode
import matplotlib.pyplot as plt
import serial.tools.list_ports


READ_SIZE = 1 # bytes
FORMAT = '<B'
SCAN_END = b'\x02'
CLEARED_BUFFER = b'\x04'
FOUND_CODE = b'\x00'
BAUDRATE = 1000000
SCAN_END_DELAY = 2

class ArduinoComm:
    def __init__(self, port=None, readsize=READ_SIZE, baudrate=BAUDRATE):
        # Find port if not specified
        if port is None: port = find_arduino_port()

        self.ser = serial.Serial(port, baudrate, timeout=None)
        self.readsize = readsize
        self.values = []

    def clear_buffer(self) -> None:
        while self.read_byte() != CLEARED_BUFFER: pass

    def read_byte(self):
        return self.ser.read(self.readsize)
    
    def write_flag(self, flag: bytes):
        self.ser.write(b'\x00')

    def close(self):
        self.ser.close()

    def __del__(self):
        self.close()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


def decode_byte(byte: bytes):
    return struct.unpack(FORMAT, byte)[0]

def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'USB' in port.description:
            return port.device
    return None

def get_sweep(comm: ArduinoComm) -> list:
    values = []
    while True:
        val = comm.read_byte()
        if val == SCAN_END:
            break
        values.append(decode_byte(val))
    return values

def get_n_sweeps(comm: ArduinoComm, n: int) -> list:
    values = []
    for _ in range(n):
        values += get_sweep(comm)
    return values

def wait_until(comm: ArduinoComm, flags: bytes) -> None:
    val = 0
    while val != flags:
        val = comm.read_byte()

def show_sweeps(comm: ArduinoComm, n: int) -> bytes:
    decoded = None
    for _ in range(n):
        values = get_sweep(comm)
        barcode = Barcode.from_sample_list(values)
        barcode.show_image()
        decoded = barcode.decode()
        print(decoded)
        if decoded: break
    return decoded

def find_barcode(comm: ArduinoComm) -> bytes:
    decoded = None
    while decoded is None:
        values = get_sweep(comm)
        barcode = Barcode.from_sample_list(values)
        decoded = barcode.decode()

    comm.write_flag(FOUND_CODE)
    comm.clear_buffer()

    return decoded

def find_barcode_test():
    time.sleep(2)
    return b'000000094122'

def work():
    with ArduinoComm() as comm:
        wait_until(comm, SCAN_END)
        while True:
            decoded = find_barcode(comm)
            time.sleep(2)
            print(decoded)
