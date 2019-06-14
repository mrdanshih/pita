import numpy as np
import json
import math
import time

GATE_COORDINATES = (3, -3)


class World:
    def __init__(self):
        self.reset()

    def reset(self):
        self.coords = (0, 0)
        self.prevCoords = (0, 0)
        self.state = (0, 0)
        self.total_reward = 0
        self.total_steps = 100
        self.sheeps = set()

        self.actions = 7
        self.prevAction = None
        self.world = np.zeros((21, 21))
        self.world_state = None
        self.shouldReturn = False
        self.holding_wheat = False

    # only allow agent to use the first 5 as actions
    def getValidActions(self):
        return [0, 1, 2, 3, 4]

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

    def agentInPen(self):
        x, z = self.state
        return 5 > x > 0 and -1 > z > -5

    def sheepInPen(self, x, z):
        return 6 > x > 0 and -1 > z > -5

    def returnToStart(self):
        x, z = self.state
        time.sleep(0.3)

        if self.agentInPen():
            if self.shouldReturn:
                self.shouldReturn = False
                return 5
            else:
                return 6

        if x > 9 and z < -1:
            return 3
        elif x < 8 and z > -3:
            return 2
        elif z > -3:
            return 0
        else:
            return 3

    def update_state(self, world_state, action, agent_host):
        self.total_steps -= 1
        self.world = np.zeros(self.world.shape)
        reward = -1

        if action not in self.getValidActions():
            print('INVALID ACCTION')
            reward -= 500

        if world_state.number_of_observations_since_last_state > 0:
            if action == 4:
                if self.prevAction == 4:    # Punish redundantly choosing show wheat
                    reward -= 200
                else:
                    reward += 50
            elif self.coords == self.prevCoords:    # Punish move actions that lead to nowhere (due to hitting border for example)
                reward -= 200

            msg = world_state.observations[-1].text
            ob = json.loads(msg)
            self.world_state = ob

            for i in ob["entities"]:

                x = round(i["x"] - 0.5)
                z = round(i["z"] - 0.5)
                if i["name"] == "Agnis":
                    self.prevCoords = self.coords
                    self.coords = (i["x"], i["z"])
                    self.world[x][z] = 1
                    self.state = (x, z)
                elif i["name"] == "Sheep":
                    # Two sheep based reward metrics:
                    row, col = self.state
                    dist = (x-row)**2 + (z-col)**2
                    if dist <= 4:
                        # # Near sheep, show wheat. (hard-coded policy when close, but agent could also learn to show it when approaching)
                        # agent_host.sendCommand("hotbar.2 1")
                        # agent_host.sendCommand("hotbar.2 0")

                        if self.sheepInPen(x, z):
                            reward += 500
                        elif i["id"] not in self.sheeps:
                            self.sheeps.add(i["id"])
                            reward += 100
                            self.shouldReturn = True
                        if action == 4:  # Good if the action shows wheat near a sheep:
                            reward += 200

                    self.world[x][z] = 2

                    # Less negative reward when agent is closer to sheep
                    reward -= dist

                    # Less negative reward when sheep is closer to "GATE"/GOAL
                    dx = i["x"] - GATE_COORDINATES[0]
                    dz = i["z"] - GATE_COORDINATES[1]
                    dist2 = math.sqrt(dx**2 + dz**2)
                    if dist2 < 50:
                        reward += 100
                    reward -= dist2
        self.prevAction = action
        self.total_reward += reward
        envstate = self.observe()
        status = self.game_status()
        return envstate, reward, status
