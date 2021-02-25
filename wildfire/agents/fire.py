from mesa import Agent
import numpy as np

from wildfire.util import *

class Fire(Agent):
    """
    Fire agent that fully spreads and dies over the course of one time step
    """

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass