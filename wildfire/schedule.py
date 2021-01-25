from collections import defaultdict
import numpy as np

from mesa.time import RandomActivation


class RandomActivationByType(RandomActivation):
    """
    A scheduler which activates each type of agent once per step, in random
    order, with the order reshuffled every step.

    Assumes that all agents have a step() method.
    """

    def __init__(self, model):
        super().__init__(model)
        self.agents_by_type = defaultdict(dict)

    def add(self, agent):
        """
        Add an Agent object to the schedule

        Args:
            agent: An Agent to be added to the schedule.
        """

        agent_class = type(agent)
        self.agents_by_type[agent_class][agent.unique_id] = agent

    def remove(self, agent):
        """
        Remove all instances of a given agent from the schedule.
        """

        agent_class = type(agent)
        del self.agents_by_type[agent_class][agent.unique_id]

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
        agent_keys = list(self.agents_by_type[agent_type].keys())
        self.model.random.shuffle(agent_keys)
        for agent_key in agent_keys:
            self.agents_by_type[agent_type][agent_key].step()

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
