import numpy as np


# General variables
INITIAL_TREES = 20
WIDTH_CELLS = 20
HEIGHT_CELLS = 20
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
CONTINUOUS_HEIGHT = 100
CONTINUOUS_WIDTH = 100

def gaussian(x, mu=0, sig=1, norm=True):
    if norm:
        return 1 / (sig * np.sqrt(2 * np.pi)) * np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
    else:
        return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))