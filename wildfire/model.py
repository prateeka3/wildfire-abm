from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from wildfire.util import *
from wildfire.agents.trees import PacificSilverFir, Tree
from wildfire.schedule import RandomActivationByType
from wildfire.space import MyContinuousSpace

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
        self.space = MyContinuousSpace(self.width, self.height, False)
        self.datacollector = DataCollector(
            {
                "Trees": lambda m: m.schedule.get_type_count(Tree)
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
            # num_seeds, in a random direction
            angle_dist = [
                (np.random.rand() * 2 * np.pi, np.random.poisson(lam=tree.tree_spacing))
                for _ in range(tree.num_seeds)
            ]
            sow_pos = [
                (
                    tree.pos[0] + np.cos(angle) * dist, # x pos
                    tree.pos[1] + np.sin(angle) * dist # y pos
                )
                for angle, dist in angle_dist
            ]
            sow_pos = list(filter(lambda pos: pos[0] > 0 and pos[0] < self.width and pos[1] > 0 and pos[1] < self.height, sow_pos))
            for pos in sow_pos:
                seed = PacificSilverFir(self.next_id(), pos, self)
                self.space.place_agent(seed, pos)
                self.schedule.add(seed)

    def run_model(self, step_count=200):
        for _ in range(step_count):
            self.step()

    def get_temp(self, x, y):
        return 58

    def get_precip(self, x, y):
        return 50
