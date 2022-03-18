import numpy as np
import matplotlib.pyplot as plt

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

def generate_barcode(code: str) -> np.array:
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

def viz_barcode(barcode: np.array, ax: plt.Axes):
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

def barcode2timeseries(barcode: np.array) -> tuple[np.array, np.array]:
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
    norm_time = ((barcode.size-1)*(time - time.min())/time.ptp()).round().astype(int)

    # Generate samples from normalized times
    samples = np.fromiter(map(lambda x: barcode[x], norm_time), dtype=bool)

    return samples, time

def timeseries2barcode():
    """
    Convert a time series to a barcode.
    """
    pass

if __name__ == '__main__':
    barcode = generate_barcode("712345678904")
    samples, time = barcode2timeseries(barcode)
    fig, (ax1, ax2) = plt.subplots(2, 1)
    viz_barcode(barcode, ax1)
    viz_timeseries(samples, time, ax2)
    plt.show()