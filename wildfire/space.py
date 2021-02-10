import numpy as np

from mesa.space import ContinuousSpace

class MyContinuousSpace(ContinuousSpace):
    def __init__(self, width, height, torus):
        super().__init__(width, height, torus)
        self.agent_x = []
        self.agent_y = []

    def place_agent(self, agent, pos):
        super().place_agent(agent, pos)
        if len(self.agent_x) == 0 | len(self.agent_y) == 0:
            self.agent_x.insert(0, (pos[0], agent))
            self.agent_y.insert(0, (pos[1], agent))
        else:
            for i, (x, _) in enumerate(self.agent_x):
                if x > pos[0] or i == len(self.agent_x)-1:
                    self.agent_x.insert(i, (pos[0], agent))
                    break
            for i, (y, _) in enumerate(self.agent_y):
                if y > pos[1] or i == len(self.agent_y)-1:
                    self.agent_y.insert(i, (pos[1], agent))
                    break

    def remove_agent(self, agent):
        self.agent_x.remove((agent.pos[0], agent))
        self.agent_y.remove((agent.pos[1], agent))

    def get_neighbors(self, pos, radius, torus):
        # Ignore torus case for now, not using it
        xmin = np.clip(pos[0]-radius, 0, self.width)
        xmax = np.clip(pos[0]+radius, 0, self.width)
        ymin = np.clip(pos[1]-radius, 0, self.height)
        ymax = np.clip(pos[1]+radius, 0, self.height)
        x_neighbs = [x[1] for x in filter(lambda x: x[0] > xmin and x[0] < xmax and x[0] != pos[0], self.agent_x)]
        y_neighbs = [y[1] for y in filter(lambda y: y[0] > ymin and y[0] < ymax and y[0] != pos[1], self.agent_y)]
        return list(set(x_neighbs) & set(y_neighbs))
        