from mesa import Agent
import numpy as np

from wildfire.util import *

class Foliage(Agent):
    """
    Foliage agent that simply sits and decays over time
    """

    def __init__(self, unique_id, pos, model, volume):
        super().__init__(unique_id, model)
        self.pos = pos
        self.volume = volume

    def step(self):
        pass