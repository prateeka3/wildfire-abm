from wildfire.agents.trees import PacificSilverFir
import numpy as np

def wildfire_portrayal(agent):
    if agent is None:
        return
    portrayal = {"Shape": "rect", "Filled": "true", "Layer": 0}

    if type(agent) is PacificSilverFir:
        portrayal['x'] = agent.pos[0]
        portrayal['y'] = agent.pos[1]
        portrayal['w'] = np.clip(agent.age/100, 0.3, 1)
        portrayal['h'] = np.clip(agent.age/100, 0.3, 1)
        portrayal["Color"] = '#00AA00'

    return portrayal