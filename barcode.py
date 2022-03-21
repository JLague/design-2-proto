import numpy as np
import matplotlib.pyplot as plt
from pyzbar import pyzbar
from PIL import Image

EDGE = '101'
MIDDLE = '01010'
CODES = {
    "L": [
        "0001101",
        "0011001",
        "0010011",
        "0111101",
        "0100011",
        "0110001",
        "0101111",
        "0111011",
        "0110111",
        "0001011",
    ],
    "R": [
        "1110010",
        "1100110",
        "1101100",
        "1000010",
        "1011100",
        "1001110",
        "1010000",
        "1000100",
        "1001000",
        "1110100",
    ],
}

CODE_LEN = 12
N_SAMPLES = 300
MEAN_SAMPLE_TIME = 0.001
VAR_SAMPLE_TIME = MEAN_SAMPLE_TIME * 100

UPC = b'7472389482343'

class Barcode:
    CODE_HEIGHT = 15

    def __init__(self, samples: np.ndarray):
        self.samples = samples
        self.samples = Barcode._invert(self.samples)
        self.samples = Barcode._expand(self.samples)
        self.shape = reversed(self.samples.shape)

    def from_samples(samples):
        return Barcode(samples)
    
    def from_num(num):
        barcode = generate_barcode(str(num))
        return Barcode(barcode2timeseries(barcode))
    
    def from_sample_list(samples: list):
        return Barcode(np.array(samples))
    
    def _expand(samples):
        """
        Expand the barcode.
        """
        samples = (samples * 255).reshape(1, -1).astype(np.uint8)
        return np.tile(samples, (Barcode.CODE_HEIGHT, 1))
    
    def decode(self):
        """
        Decode a barcode.

        Returns:
            The decoded code.
        """
        image = (self.samples.tobytes(), *self.shape)
        dec = pyzbar.decode(image, symbols=[pyzbar.ZBarSymbol.EAN13])
        return dec[0].data[1:] if dec else None
    
    def show_image(self) -> None:
        """
        Get the barcode as a PIL image.
        """
        Image.fromarray(self.samples).show()
    
    def _invert(samples):
        """
        Invert the barcode.
        """
        return np.logical_not(samples)

def generate_barcode(code: str) -> np.ndarray:
    """
    Generate a barcode from a code.
    """
    # Check if code size is valid
    if len(code) != CODE_LEN:
        raise ValueError("Invalid code length")
    
    # Generate barcode
    barcode = []
    barcode.append(EDGE)
    for c in code[:CODE_LEN//2]:
        barcode.append(CODES['L'][int(c)])
    barcode.append(MIDDLE)
    for c in code[CODE_LEN//2:]:
        barcode.append(CODES['R'][int(c)])
    barcode.append(EDGE)

    # Convert to numpy array
    barcode = np.array([True if c == '1' else False for c in ''.join(barcode)])

    return barcode

def viz_barcode(barcode: np.ndarray, ax: plt.Axes):
    """
    Visualize a barcode.
    """
    barprops = dict(aspect='auto', cmap='binary', interpolation='nearest')
    ax.set_title('Code UPC-A')
    ax.set_axis_off()
    return ax.imshow(barcode.reshape(1, -1), **barprops)

def viz_timeseries(values: np.array, time: np.array, ax: plt.Axes):
    """
    Visualize a time series.
    """
    ax.set_title('Code-barres échantillonné')
    ax.set_axis_off()
    return ax.fill_between(time, values, step='mid')

def barcode2timeseries(barcode: np.ndarray) -> np.ndarray:
    """
    Convert a barcode to a time series.

    Returns:
        A tuple of (barcode samples, times).
    """
    # Generate random sample times
    rng = np.random.default_rng()
    alpha = VAR_SAMPLE_TIME / MEAN_SAMPLE_TIME
    beta = MEAN_SAMPLE_TIME ** 2 / VAR_SAMPLE_TIME
    time_deltas = rng.gamma(alpha, beta, N_SAMPLES)
    time = np.cumsum(time_deltas)

    # Normalize times to barcode size
    norm_time = (barcode.size*(time - time.min())/time.max()).astype(int)

    # Generate samples from normalized times
    samples = np.fromiter(map(lambda x: barcode[x], norm_time), dtype=bool)

    return samples

# def decode_barcode(barcode: np.ndarray) -> bytes:
#     """
#     Decode a barcode.

#     Returns:
#         The decoded code.
#     """
#     barcode = (barcode * 255).reshape(1, -1).astype(np.uint8)
#     barcode = np.tile(barcode, (CODE_HEIGHT, 1))
#     image = (barcode.tobytes(), *reversed(barcode.shape))
#     dec = pyzbar.decode(image, symbols=[pyzbar.ZBarSymbol.EAN13])
#     return dec[0].data[1:] if dec else None

def invert(barcode: np.ndarray) -> np.ndarray:
    """
    Invert a barcode.
    """
    return np.logical_not(barcode)


if __name__ == '__main__':
    # with open('data/barcode.txt', 'r') as f:
    #     array = np.loadtxt(f, delimiter=",")
    # barcode = array[:, 0]
    barcode = Barcode.from_num(724771001911)
    # barcode = invert(generate_barcode("712345678904"))
    # samples = barcode2timeseries(barcode)
    print(barcode.decode().decode('utf-8'))
    # fig, (ax1, ax2) = plt.subplots(2, 1)
    # viz_barcode(barcode, ax1)
    # viz_timeseries(samples, ax2)
    # plt.show()