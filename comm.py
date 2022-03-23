import time
import serial
import struct
from barcode import Barcode
import matplotlib.pyplot as plt
import serial.tools.list_ports
from audio import play_sound, Sound


READ_SIZE = 1 # bytes
FORMAT = '<B'
SWEEP_END = b'\x02'
PATTERN_END = b'\x03'
BAUDRATE = 1000000

class ArduinoComm:
    def __init__(self, port=None, readsize=READ_SIZE, baudrate=BAUDRATE):
        if port is None: port = find_arduino_port()
        self.ser = serial.Serial(port, baudrate, timeout=None)
        self.readsize = readsize
        self.format = format
        self.values = []


    def read(self):
        return self.ser.read(self.readsize)
    
    def write(self):
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
        val = comm.read()
        if val == SWEEP_END:
            break
        values.append(decode_byte(val))
    # values = values[len(values)//4+200:len(values)//2+100]
    return values

def get_n_sweeps(comm: ArduinoComm, n: int) -> list:
    values = []
    for _ in range(n):
        values += get_sweep(comm)
    return values

def wait_until(comm: ArduinoComm, flags: bytes) -> None:
    val = 0
    while val != flags:
        val = comm.read()

def show_sweeps(comm: ArduinoComm, n: int):
    decoded = None
    for _ in range(n):
        values = get_sweep(comm)
        barcode = Barcode.from_sample_list(values)
        barcode.show_image()
        decoded = barcode.decode()
        print(decoded)
        if decoded: break
    return decoded

def find_barcode(comm: ArduinoComm):
    decoded = None
    while decoded is None:
        values = get_sweep(comm)
        barcode = Barcode.from_sample_list(values)
        decoded = barcode.decode()
    comm.write()
    comm.ser.flushInput()
    play_sound(Sound.CONFIRM)
    time.sleep(1)
    return decoded


if __name__ == '__main__':
    decoded = None
    with ArduinoComm() as comm:
        # decoded = show_sweeps(comm, 10)
        while True:
            decoded = find_barcode(comm)
            print(decoded)
