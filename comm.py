import serial
import struct
from barcode import Barcode, barcode2timeseries
import matplotlib.pyplot as plt
import serial.tools.list_ports


READ_SIZE = 1 # bytes
FORMAT = '<B'
SWEEP_END = b'\x02'
PATTERN_END = b'\x03'

class ArduinoComm:
    def __init__(self, port=None, readsize=READ_SIZE):
        if port is None: port = find_arduino_port()
        self.ser = serial.Serial(port, 115200, timeout=None)
        self.readsize = readsize
        self.format = format
        self.values = []


    def read(self):
        return self.ser.read(self.readsize)
        # return struct.unpack(self.format, self.ser.read(1))[0]

    def close(self):
        self.ser.close()

    def __del__(self):
        self.close()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    # def work(self):
    #     while True:
    #         # Read data
    #         val, flags = self.read()
    #         self.values.append(val)

    #         # If pass is finished
    #         if flags != 0:
    #             self.ax.plot(self.values, 'r')
    #             self.fig.canvas.draw()
    #             self.fig.canvas.flush_events()
    #             # analyze_data(self.values, self.times)
    #             self.values.clear()
    

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
    return values

def get_n_sweeps(comm: ArduinoComm, n: int) -> list:
    values = []
    for _ in range(n):
        values += get_sweep(comm)
    return values

def wait_until(flags: bytes) -> None:
    val = 0
    while val != flags:
        val = comm.read()


if __name__ == '__main__':
    with ArduinoComm() as comm:
        wait_until(SWEEP_END)
        samples = get_n_sweeps(comm, 2)
        barcode = Barcode.from_sample_list(samples)
        print(barcode.decode())
        

# if __name__ == '__main__':
#     with ArduinoComm() as comm:
#         code = []
#         flags = 0
#         while flags == 0:
#             val = comm.read()
#             if val == 2:
#                 print(val)
#                 flags = 1
#             else: flag = 0
#         flags = 0
#         for _ in range(10):
#             flags = 0
#             code.clear()
#             while flags == 0:
#                 val = comm.read()
#                 if val == 2:
#                     flags = 1
#                 else: flag = 0
#                 code.append(val)
#                 if flags:
#                     pass
#                     # print(code)
#                     # print(Barcode.from_sample_list(code).decode())
#         # print(len(code))
#         # print(code)
#         flags = 0
#         while flags == 0:
#                 val = comm.read()
#                 if val == 2:
#                     flags = 1
#                 else: flag = 0
#                 code.append(val)
#         print(Barcode.from_sample_list(code).decode())