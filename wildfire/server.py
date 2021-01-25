from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from wildfire.agents.trees import PacificSilverFir
from wildfire.model import Wildfire
from wildfire.portrayal.viz import wildfire_portrayal
from wildfire.util import *


canvas_element = CanvasGrid(wildfire_portrayal, WIDTH_CELLS, HEIGHT_CELLS, GRID_WIDTH, GRID_HEIGHT)
num_firs_chart = ChartModule(
    [{"Label": "Pacific Silver Firs", "Color": "#00AA00"}]
)
height_firs_chart = ChartModule(
    [{"Label": "Pacific Silver Fir Height", "Color": "#0000AA"}]
)

model_params = {
    "height": HEIGHT_CELLS,
    "width": WIDTH_CELLS,
}

server = ModularServer(
    Wildfire, [canvas_element, num_firs_chart, height_firs_chart], "Wildfire Spread", model_params
)
server.port = 8521
