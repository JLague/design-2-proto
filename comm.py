import serial
import struct
import time
import matplotlib.pyplot as plt
import serial.tools.list_ports

READ_SIZE = 3 # bytes
FORMAT = '<HB'

class ArduinoComm:
    def __init__(self, port=None, readsize=READ_SIZE, format=FORMAT):
        if port is None: port = find_arduino_port()
        self.ser = serial.Serial(port, 115200, timeout=None)
        self.readsize = readsize
        self.format = format
        self.values = []
        # plt.ion()
        # self.fig = plt.figure()
        # self.ax = self.fig.add_subplot(111)

    def read(self) -> tuple(int, int):
        data = self.ser.read(self.readsize)
        return struct.unpack(self.format, data)

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
    

def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'Arduino' in port.description:
            return port.device
    return None
