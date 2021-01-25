from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from wildfire.util import *
from wildfire.agents.trees import PacificSilverFir
from wildfire.schedule import RandomActivationByType

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
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.datacollector = DataCollector(
            {
                "Pacific Silver Firs": lambda m: m.schedule.get_type_count(PacificSilverFir),
                "Pacific Silver Fir Height": lambda m: m.schedule.get_avg_height(PacificSilverFir)
            }
        )

        # Create Trees:
        for _ in range(initial_trees):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            tree = PacificSilverFir(self.next_id(), (x, y), self)
            self.grid.place_agent(tree, (x, y))
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

    def disperse_seeds(self, tree, neighbors):
        if type(tree) == PacificSilverFir:
            for n in neighbors:
                if self.grid.is_cell_empty(n):
                    seed = PacificSilverFir(self.next_id(), n, self)
                    self.grid.place_agent(seed, n)
                    self.schedule.add(seed)

    def run_model(self, step_count=200):
        for _ in range(step_count):
            self.step()

    def get_temp(self, x, y):
        return 53

    def get_precip(self, x, y):
        return 50
