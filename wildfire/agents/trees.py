from mesa import Agent
import numpy as np

from wildfire.util import *

class Tree(Agent):
    """
    Tree that may have different requirements for growth/growth rates
    """

    def __init__(self, unique_id, pos, model, age=-2, height=0, diameter=0,
                 precip=(0,100), temp=(50, 60), reproduction_height=10,
                 max_diameter=10, max_age=100, max_height=100, tree_spacing=10,
                 p=3, k_range=(0.01, 0.02), num_seeds=5):
        super().__init__(unique_id, model)
        # inits
        self.pos = pos
        self.age = age
        self.height = height
        self.diameter = diameter

        # Ideal Climate
        self.precip = precip # inches per year
        self.temp = temp # average summer temp, Farenheit

        # Tree-Specific Params
        self.max_diameter = max_diameter # inches
        self.max_age = max_age # years
        self.max_height = max_height # feet
        self.tree_spacing = tree_spacing # ideal spacing between trees. determines dispersal as well as required sunlight
        self.k_range = k_range
        self.p = p
        self.num_seeds = num_seeds
        self.reproduction_height = reproduction_height

        # Derived Characteristics
        self.temp_mean = (self.temp[1] + self.temp[0])/2
        self.temp_sd = (self.temp[1] - self.temp[0])/2
        self.precip_mean = (self.precip[1] + self.precip[0])/2
        self.precip_sd = (self.precip[1] - self.precip[0])/2
        self.max_radius_increase = self.max_diameter/(2*self.max_age)

    def step(self):
        total_adverse_diff = self.calculate_adverse_effects()

        # if new seed, die if not in good conditions
        if self.age <= 0 and -total_adverse_diff + np.random.standard_normal() > 0:
            self.die()
            return

        k = self.k_range[1] - total_adverse_diff * (self.k_range[1] - self.k_range[0])

        if k < 0:
            self.die()
            return

        self.age += 1

        dh = self.max_height * k * self.p * np.exp(-k*self.age) * (1 - np.exp(-k*self.age))**(self.p-1)
        self.height += dh
        dr = self.max_radius_increase * k / (self.k_range[1] - self.k_range[0])
        self.diameter += dr

        if self.height >= self.reproduction_height:
            self.model.disperse_seeds(self)

    def calculate_adverse_effects(self):
        # Calculate differences from ideal environment
        z_t = np.abs(self.model.get_temp(*self.pos) - self.temp_mean) / self.temp_sd
        z_p = np.abs(self.model.get_precip(*self.pos) - self.precip_mean) / self.precip_sd
        # sunlight based on nearby trees. inverse weighted sum of neighboring heights
        curr_spacing = self.tree_spacing# * 4 * (self.height / self.max_height)
        neighbors = self.model.space.get_neighbors(self.pos, curr_spacing, False)
        weighted_neighbor_height = np.sum([1 / self.model.space.get_distance(self.pos, n.pos) * curr_spacing * n.height for n in neighbors])
        competing_height_diff = weighted_neighbor_height - self.height
        reduced_sunlight = np.clip(competing_height_diff, 0, None)

        max_adverse_effects = 3 # number of above variables
        return (z_t + z_p + reduced_sunlight) / max_adverse_effects

    def die(self):
        self.model.schedule.remove(self)
        self.model.space.remove_agent(self)

    def get_volume(self):
        return self.height * (self.diameter / 2)**2 * np.pi

class PacificSilverFir(Tree):
    """
    https://plants.usda.gov/plantguide/pdf/pg_abam.pdf
    """

    def __init__(self, unique_id, pos, model, age=-2, height=0, diameter=0):
        super().__init__(
            unique_id,
            pos,
            model,
            age=age,
            height=height,
            diameter=diameter,
            precip=(40, 260),
            temp=(57, 59),
            reproduction_height=12,
            tree_spacing=10,
            max_diameter=45,
            max_age=400,
            max_height=230,
            k_range=(0.01, 0.022),
            num_seeds=5
            )