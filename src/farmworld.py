import numpy as np
import json
import math

GATE_COORDINATES = (0,0)

class World:
    def __init__(self):
        self.reset()

    def reset(self):
        self.coords = (0, 0)
        self.state = (0, 0)
        self.total_reward = 0
        self.total_steps = 50
        self.sheeps = set()
        self.actionMap = {0: 'movenorth 1', 1: 'movesouth 1',
                          2: 'moveeast 1', 3: 'movewest 1'}
                          # 4: 'hold_wheat', 5: 'hide_wheat'}
        self.actions = [k for k in self.actionMap]
        self.world = np.zeros((16, 16))
        self.world_state = None

    def getValidActions(self):
        result = []
        for act_id, action in self.actionMap.items():
            my_x, my_z = self.state
            if act_id == 0 and my_z <= 0:
                continue
            if act_id == 1 and my_z >= 14:
                continue
            if act_id == 2 and my_x >= 14:
                continue
            if act_id == 3 and my_x <= 0:
                continue
            result.append(act_id)
        return result

    def num_actions(self):
        return len(self.actions)

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

    def isSheepInPen(self, entity):
        x = entity["x"]
        z = entity["z"]
        return 1 <  x < 5 and 1 < z < 5
    def update_state(self, world_state, action, agent_host):
        self.total_steps -= 1
        self.world = np.zeros(self.world.shape)
        reward = -1

        if action not in self.getValidActions():
            print('INVALID ACCTION')
            reward -= 500

        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            ob = json.loads(msg)
            self.world_state = ob
            for i in ob["entities"]:
       

                x = round(i["x"] - 0.5)
                z = round(i["z"] - 0.5)
                if i["name"] == "Agnis":
                    self.coords = (i["x"], i["z"])
                    self.world[x][z] = 1
                    self.state = (x, z)
                elif i["name"] == "Sheep":
                    # Two sheep based reward metrics:
                    row, col = self.state
                    dist = (x-row)**2 + (z-col)**2
                    if dist <= 4:
                        if (row, col) == (0, 0):
                            reward += 300
                        elif i["id"] not in self.sheeps:
                            self.sheeps.add(i["id"])
                            reward += 100
                    self.world[x][z] = 2

                    # Less negative reward when agent is closer to sheep
                    reward -= dist
                    
                    # Less negative reward when sheep is closer to "GATE"/GOAL
                    dx = i["x"] - GATE_COORDINATES[0]
                    dz = i["z"] - GATE_COORDINATES[1]
                    dist2 = (dx**2 + dz**2)
                    if dist2 < 50:
                        reward += 100
                    reward -= dist2

        self.total_reward += reward
        envstate = self.observe()
        status = self.game_status()
        return envstate, reward, status
