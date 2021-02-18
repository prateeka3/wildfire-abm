from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from wildfire.agents.trees import PacificSilverFir
from wildfire.model import Wildfire
from wildfire.portrayal.viz import wildfire_portrayal
from wildfire.portrayal.SimpleContinuousModule import SimpleCanvas
from wildfire.util import CANVAS_HEIGHT, CANVAS_WIDTH, CONTINUOUS_HEIGHT, CONTINUOUS_WIDTH

canvas_element = SimpleCanvas(wildfire_portrayal, CANVAS_HEIGHT, CANVAS_WIDTH)
num_firs_chart = ChartModule(
    [{"Label": "Trees", "Color": "#00AA00"}]
)
model_params = {
    "height": CONTINUOUS_HEIGHT,
    "width": CONTINUOUS_WIDTH,
}

server = ModularServer(
    Wildfire, [canvas_element, num_firs_chart], "Wildfire Spread", model_params
)
server.port = 8521
