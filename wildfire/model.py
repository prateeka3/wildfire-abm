from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from wildfire.util import *
from wildfire.agents.trees import PacificSilverFir, Tree
from wildfire.agents.foliage import Foliage
from wildfire.schedule import RandomActivationByType
from mesa.space import ContinuousSpace

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
        # num_seeds, in a random direction
        sow_pos = get_poisson_random_positions(
            tree.pos[0], tree.pos[1], tree.tree_spacing,
            tree.num_seeds, self.width, self.height
        )
        
        if type(tree) == PacificSilverFir:
            for pos in sow_pos:
                seed = PacificSilverFir(self.next_id(), pos, self)
                self.space.place_agent(seed, pos)
                self.schedule.add(seed)

    def drop_foliage(self, tree):
        volume = tree.foliage_prop * tree.get_volume()
        pos = get_poisson_random_positions(
            tree.pos[0], tree.pos[1], tree.tree_spacing,
            3, self.width, self.height
        )[0]
        foliage = Foliage(self.next_id(), pos, self, volume)
        print(pos)
        self.space.place_agent(foliage, pos)
        self.schedule.add(foliage)


    def run_model(self, step_count=200):
        for _ in range(step_count):
            self.step()

    def get_temp(self, x, y):
        return 58

    def get_precip(self, x, y):
        return 50
