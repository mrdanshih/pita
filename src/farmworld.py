import numpy as np
import json


class World:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = (0, 0)
        self.total_reward = 0
        self.total_steps = 50
        self.sheeps = set()
        self.actions = [0, 1, 2, 3]
        self.actionMap = {0: 'movenorth 1', 1: 'movesouth 1',
                          2: 'moveeast 1', 3: 'movewest 1'}
        self.world = np.zeros((10, 10))

    def game_status(self):
        if self.total_steps > 0:
            if self.total_reward > 200:
                return "win"
            else:
                return "playing"
        else:
            if self.total_reward > 0:
                return "win"
            else:
                return "lose"

    def observe(self):
        return self.world.reshape(-1)

    def update_state(self, world_state):
        self.total_steps -= 1
        self.world = np.zeros((10, 10))
        reward = -1
        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            ob = json.loads(msg)
            for i in ob["entities"]:
                x = round(i["x"] - 0.5)
                z = round(i["z"] - 0.5)
                if i["name"] == "Agnis":
                    self.world[x][z] = 1
                    self.state = (x, z)
                elif i["name"] == "Sheep":
                    row, col = self.state
                    dist = (x-row)**2 + (z-col)**2
                    if dist <= 4:
                        if (row, col) == (0, 0):
                            reward = 200
                        elif i["id"] not in self.sheeps:
                            self.sheeps.add(i["id"])
                            reward = 20
                    self.world[x][z] = 2
        self.total_reward += reward
        envstate = self.observe()
        status = self.game_status()
        return envstate, reward, status
