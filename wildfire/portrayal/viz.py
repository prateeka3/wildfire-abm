from wildfire.agents.trees import PacificSilverFir
import numpy as np

def wildfire_portrayal(agent):
    if agent is None:
        return
    portrayal = {"Shape": "circle", "Filled": "true", "Layer": 0}

    if type(agent) is PacificSilverFir:
        portrayal['x'] = agent.pos[0]
        portrayal['y'] = agent.pos[1]
        portrayal['r'] = int(np.clip(agent.diameter, 1, 30))
        portrayal["Color"] = '#00AA00'

    return portrayal