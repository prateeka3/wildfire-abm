from mesa import Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector

from wildfire.util import *
from wildfire.agents.trees import PacificSilverFir
from wildfire.schedule import RandomActivationByType

import numpy as np

class Wildfire(Model):
    """
    Wildfire Model
    """

    height = 20
    width = 20

    verbose = False  # Print-monitoring

    description = (
        "A model for forests and wildfires."
    )

    def __init__(
        self,
        height=20,
        width=20,
        initial_trees=INITIAL_TREES,
    ):
        """
        Create a new Wildfire model with the given parameters.

        Args:
            
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width

        self.schedule = RandomActivationByType(self)
        self.space = ContinuousSpace(self.width, self.height, False)
        self.datacollector = DataCollector(
            {
                "Pacific Silver Firs": lambda m: m.schedule.get_type_count(PacificSilverFir),
                "Pacific Silver Fir Height": lambda m: m.schedule.get_avg_height(PacificSilverFir)
            }
        )

        # Create Trees:
        for _ in range(initial_trees):
            x = np.random.rand() * self.width
            y = np.random.rand() * self.height
            tree = PacificSilverFir(self.next_id(), (x, y), self)
            self.space.place_agent(tree, (x, y))
            self.schedule.add(tree)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    self.schedule.get_type_count(PacificSilverFir),
                ]
            )

    def disperse_seeds(self, tree):
        if type(tree) == PacificSilverFir:
            # fix this, disperse in a neighborhood
            sow_pos = []
            for p in sow_pos:
                seed = PacificSilverFir(self.next_id(), p, self)
                self.space.place_agent(seed, p)
                self.schedule.add(seed)

    def run_model(self, step_count=200):
        for _ in range(step_count):
            self.step()

    def get_temp(self, x, y):
        return 53

    def get_precip(self, x, y):
        return 50
