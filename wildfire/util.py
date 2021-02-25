import numpy as np


# General variables
INITIAL_TREES = 20
WIDTH_CELLS = 20
HEIGHT_CELLS = 20
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
CONTINUOUS_HEIGHT = 200
CONTINUOUS_WIDTH = 200

def gaussian(x, mu=0, sig=1, norm=True):
    if norm:
        return 1 / (sig * np.sqrt(2 * np.pi)) * np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
    else:
        return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


def get_poisson_random_positions(x, y, lam, num_pos, max_x, max_y):
    angle_dist = [
        (np.random.rand() * 2 * np.pi, np.random.poisson(lam=lam))
        for _ in range(num_pos)
    ]
    sow_pos = [
        (
            x + np.cos(angle) * dist, # x pos
            y + np.sin(angle) * dist # y pos
        )
        for angle, dist in angle_dist
    ]
    print(sow_pos)
    sow_pos = list(filter(lambda pos: pos[0] > 0 and pos[0] < max_x and pos[1] > 0 and pos[1] < max_y, sow_pos))

    return sow_pos