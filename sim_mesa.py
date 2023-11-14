from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
import random

GRID_SIZE = 10
INIT_WOLVES = 2
INIT_DEER = 5
WOLF_SPEED = 1
DEER_SPEED = 1


class Animal(Agent):
    def __init__(self, unique_id, model, speed):
        super().__init__(unique_id, model)
        self.speed = speed

    def move(self, dx, dy):
        new_position = ((self.pos[0] + dx) % GRID_SIZE, (self.pos[1] + dy) % GRID_SIZE)
        self.model.grid.move_agent(self, new_position)


class Wolf(Animal):
    def step(self):
        deer_positions = [
            agent.pos for agent in self.model.schedule.agents if isinstance(agent, Deer)
        ]
        if not deer_positions:  # No deer left
            print("no deer")
            return

        nearest_deer_pos = min(
            deer_positions,
            key=lambda x: abs(self.pos[0] - x[0]) + abs(self.pos[1] - x[1]),
        )
        dx = dy = 0
        if nearest_deer_pos[0] > self.pos[0]:
            dx = 1
        elif nearest_deer_pos[0] < self.pos[0]:
            dx = -1
        if nearest_deer_pos[1] > self.pos[1]:
            dy = 1
        elif nearest_deer_pos[1] < self.pos[1]:
            dy = -1
        self.move(dx * self.speed, dy * self.speed)

        # Check if wolf caught any deer
        cell_mates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cell_mates:
            if isinstance(agent, Deer):
                self.model.to_be_removed.add(agent)


class Deer(Animal):
    def step(self):
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        self.move(dx * self.speed, dy * self.speed)


class WolfDeerModel(Model):
    def __init__(self, N_W, N_D):
        self.grid = MultiGrid(GRID_SIZE, GRID_SIZE, torus=True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.datacollector = DataCollector(model_reporters={"Deer": compute_deer_count})
        self.to_be_removed = set()

        # Create wolves
        for i in range(N_W):
            wolf = Wolf(i, self, WOLF_SPEED)
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(wolf, (x, y))
            self.schedule.add(wolf)

        # Create deer
        for i in range(N_D):
            deer = Deer(
                i + N_W, self, DEER_SPEED
            )  # Continue id numbering from where wolves left off
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(deer, (x, y))
            self.schedule.add(deer)

    def step(self):
        self.schedule.step()
        for agent in self.to_be_removed:
            self.schedule.remove(agent)
            self.grid.remove_agent(agent)
        self.to_be_removed.clear()
        self.datacollector.collect(self)


# Run the model
# model = WolfDeerModel(INIT_WOLVES, INIT_DEER)
# for i in range(100):  # Run for 100 steps
#     model.step()


def compute_deer_count(model):
    return len([agent for agent in model.schedule.agents if isinstance(agent, Deer)])


def agent_portrayal(agent):
    if isinstance(agent, Wolf):
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "r": 0.5,
            "Color": "red",
            "Layer": 1,
        }
    elif isinstance(agent, Deer):
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "r": 0.5,
            "Color": "green",
            "Layer": 0,
        }
    return portrayal


grid = CanvasGrid(agent_portrayal, GRID_SIZE, GRID_SIZE, 500, 500)

chart = ChartModule(
    [{"Label": "Deer", "Color": "red"}], data_collector_name="datacollector"
)

server = ModularServer(
    WolfDeerModel,
    [grid, chart],
    "Wolf-Deer Model",
    {"N_W": INIT_WOLVES, "N_D": INIT_DEER},
)

server.launch(port=5000)
