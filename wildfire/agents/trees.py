from mesa import Agent
import numpy as np

class Tree(Agent):
    """
    Tree that may have different requirements for growth/growth rates
    """

    def __init__(self, unique_id, pos, model, age=0, height=0, diameter=0,
                 precip=(0,100), temp=(50, 60), reproduction_age=20, reproduction_sd=3,
                 max_diameter=10, max_age=100, max_height=100, max_height_difference=5,
                 p=3, k_range=(0.01, 0.02)):
        super().__init__(unique_id, model)
        self.pos = pos
        self.age = age
        self.height = height
        self.diameter = diameter
        self.precip = precip # inches per year
        self.temp = temp # average summer temp, Farenheit
        self.max_diameter = max_diameter # inches
        self.max_age = max_age # years
        self.max_height = max_height # feet
        self.max_height_difference = max_height_difference # max height difference to avg height of surrounding trees to determine amount of sunlight
        self.p = p
        self.k_range = k_range

        self.reproduction_age = reproduction_age + reproduction_sd * np.random.standard_normal() # years old, when it starts reproducing
        self.temp_mean = (self.temp[1] + self.temp[0])/2
        self.temp_sd = (self.temp[1] - self.temp[0])/2
        self.precip_mean = (self.precip[1] + self.precip[0])/2
        self.precip_sd = (self.precip[1] - self.precip[0])/2

    def step(self):
        total_adverse_diff = self.calculate_adverse_effects()

        # if new seed, die if not in good conditions
        if self.age == 0 and total_adverse_diff + np.random.standard_normal() > 0:
            self.die()
            return

        # Shift normal of k based on amount of adversity in environment. SD is half of k range
        middle_k = (self.k_range[1] - self.k_range[0]) / 2 + self.k_range[0]
        k = self.calc_new_k(middle_k - total_adverse_diff)
        dr = self.calc_new_k(self.max_diameter/(2*self.max_age))
        
        self.age += 1
        self.diameter += dr

        height_delta = self.max_height * k * self.p * np.exp(-k*self.age) * (1 - np.exp(-k*self.age))**(self.p-1)
        if height_delta < 0:
            print(height_delta)
            self.die()
            return
        self.height += height_delta

        if self.age >= self.reproduction_age:
            neighbors = self.model.grid.iter_neighborhood(self.pos, moore=True, include_center=False)
            self.model.disperse_seeds(self, neighbors)

    def calculate_adverse_effects(self):
        # Calculate differences from ideal environment
        z_t = np.abs((self.model.get_temp(*self.pos) - self.temp_mean)/self.temp_sd) # max allowable: 1
        z_p = np.abs((self.model.get_precip(*self.pos) - self.precip_mean)/self.precip_sd) # max allowable: 1
        # sunlight based on nearby trees
        competing_height_diff = self.avg_neighbor_height() - self.height
        reduced_sunlight = np.clip(competing_height_diff, 0, None)/self.max_height_difference

        max_adverse_effects = 3 # sum of max allowable amounts of above variables
        x = (z_t + z_p + reduced_sunlight) / max_adverse_effects * (self.k_range[1] - self.k_range[0])
        return x

    def calc_new_k(self, total_adverse_diff):
        mu = total_adverse_diff
        sd = (self.k_range[1] - self.k_range[0])/2
        rv = mu + sd * np.random.standard_normal()
        return np.clip(rv, *self.k_range)

    def die(self):
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)

    def avg_neighbor_height(self):
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
        sum_height = 0
        for n in neighbors:
            if issubclass(type(n), Tree):
                sum_height += n.height
        return sum_height / 8

    def get_volume(self):
        return self.height * (self.diameter / 2)**2 * np.pi

class PacificSilverFir(Tree):
    """
    https://plants.usda.gov/plantguide/pdf/pg_abam.pdf
    """

    def __init__(self, unique_id, pos, model, age=0, height=0, diameter=0):
        super().__init__(
            unique_id,
            pos,
            model,
            age=age,
            height=height,
            diameter=diameter,
            precip=(40, 260),
            temp=(57, 59),
            reproduction_age=20,
            reproduction_sd=3,
            max_diameter=45,
            max_age=400,
            max_height=230,
            max_height_difference=1,
            k_range=(0.01, 0.022)
            )