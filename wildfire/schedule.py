from collections import defaultdict
import numpy as np
import pandas as pd
import time

from mesa.time import RandomActivation

from wildfire.agents.trees import Tree


class RandomActivationByType(RandomActivation):
    """
    A scheduler which activates each type of agent once per step, in random
    order, with the order reshuffled every step.

    Assumes that all agents have a step() method.
    """

    def __init__(self, model):
        super().__init__(model)
        self.agents_by_type = defaultdict(dict)
        self.distances = np.empty(shape=[0,0])
        self.num_agents = 0

        self.step_times = []

    def add(self, agent):
        """
        Add an Agent object to the schedule

        Args:
            agent: An Agent to be added to the schedule.
        """

        agent_class = type(agent)
        if issubclass(agent_class, Tree):
            agent_class = Tree
        self.agents_by_type[agent_class][agent.unique_id] = agent
        self.num_agents += 1

    def remove(self, agent):
        """
        Remove all instances of a given agent from the schedule.
        """

        agent_class = type(agent)
        if issubclass(agent_class, Tree):
            agent_class = Tree
        del self.agents_by_type[agent_class][agent.unique_id]
        self.num_agents -= 1

    def step(self, by_type=True):
        """
        Executes the step of each agent breed, one at a time, in random order.

        Args:
            by_breed: If True, run all agents of a single breed before running
                      the next one.
        """
        if by_type:
            for agent_class in self.agents_by_type:
                self.step_type(agent_class)
            self.steps += 1
        else:
            super().step()

    def step_type(self, agent_type):
        """
        Shuffle order and run all agents of a given type.

        Args:
            agent_type: Type of agent to run.
        """
        agents = list(self.agents_by_type[agent_type].values())
        if agent_type == Tree:
            # order by increasing age
            agents = sorted(agents, key=lambda a: a.age)
        else:
            self.model.random.shuffle(agents)

        for agent in agents:
            agent.step()

    def get_type_count(self, agent_type):
        """
        Returns the current number of agents of certain type in the queue.
        """
        return len(self.agents_by_type[agent_type].values())

    def get_avg_height(self, agent_type):
        """
        Returns average height of the agent type (tree)
        """
        return np.mean([t.height for t in self.agents_by_type[agent_type].values()])

    
