from __future__ import print_function
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #2: Run simple mission using raw XML

from builtins import range
from enum import Enum
import MalmoPython
import os
import sys
import time
import json
import math

agent_host = MalmoPython.AgentHost()
my_mission = None
my_mission_record = None


class MyAgent:
    def __init__(self, world_state):
        self.reward = 0
        self.captured_sheeps = set()
        self.visited_sheeps = set()
        self.world_state = None
        self.x = 0.5  # for discrete movement, agent has to start in middle of the block 0.5, 0.5
        self.z = 0.5
        self.prev_a = ""  # continue previous action before starting a new one
        # stall because if you keep moving, you move too fast and the sheep doesnt follow
        self.stall = False
        self.holdingWheat = False

    def isSheepInPen(self, entity):
        x = entity["x"]
        z = entity["z"]
        return 1 <  x < 5 and 1 < z < 5

    def characterMoved(self, entity):
        x = entity["x"]
        z = entity["z"]
        return not (x == self.x and z == self.z)

    def swapOutWheat(self):
        if self.holdingWheat:
            # assumes wheat is in slot 2 so to stop holding wheat switch the slot to 1
            agent_host.sendCommand("hotbar.1 1")
            agent_host.sendCommand("hotbar.1 0")
        else:
            agent_host.sendCommand("hotbar.2 1")
            agent_host.sendCommand("hotbar.2 0")

        self.holdingWheat = not self.holdingWheat
        return "swapping wheat"

    def navigateToSheep(self, sheepID):
        # my shitty dijkstras algorithm lmao
        for entity in self.world_state["entities"]:
            if entity["id"] == sheepID:
                dx = entity["x"] - self.x
                dz = entity["z"] - self.z
                dist = dx**2 + dz**2
                if (dist < 4):
                    self.prev_a = ""
                    self.visited_sheeps.add(sheepID)
                    return ""
                if abs(dx) > abs(dz):
                    if dx > 0:
                        return "moveeast 1"
                    else:
                        return "movewest 1"
                else:
                    if dz > 0:
                        return "movesouth 1"
                    else:
                        return "movenorth 1"

    def teleportToSheep(self, sheepID):
        for entity in self.world_state["entities"]:
            if entity["id"] == sheepID:
                self.swapOutWheat()
                return "tp " + str(entity["x"]) + " 4 " + str(entity["z"])

    def updateReward(self):
        for entity in self.world_state["entities"]:
            if entity["name"] == "Sheep" and entity["id"] not in self.captured_sheeps and self.isSheepInPen(entity):
                self.reward += 100
                self.captured_sheeps.add(entity["id"])
            elif entity["name"] == "Agnis" and self.characterMoved(entity):
                self.reward -= 1

    def takeAction(self):
        # if self.stall == True:
        #     print("Let's stall!")
        #     self.stall = False
        #     return ""
        # else:
        self.stall = True
        if self.prev_a:
            print("Navigate to sheep")
            return self.navigateToSheep(self.prev_a)
        for e in self.world_state["entities"]:
            if not self.holdingWheat:
                return self.swapOutWheat()
            if e["name"] == "Sheep" and not self.isSheepInPen(e) and not e["id"] in self.visited_sheeps:
                self.prev_a = e["id"]
                print("teleport to sheep")
                return self.teleportToSheep(e["id"])
        return ""

    def updateCharacter(self, world_state):
        for e in world_state["entities"]:
            if e["name"] == "Agnis":
                self.x = e["x"]
                self.z = e["z"]

    def updateWorldState(self, world_state):
        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            ob = json.loads(msg)
            self.world_state = ob
            self.updateCharacter(ob)
            self.updateReward()


def setupMission():
    mission_file = './farm.xml'
    global my_mission, my_mission_record
    with open(mission_file, 'r') as f:
        print("Loading mission from %s" % mission_file)
        mission_xml = f.read()
        my_mission = MalmoPython.MissionSpec(mission_xml, True)

    my_mission_record = MalmoPython.MissionRecordSpec()


# Attempt to start a mission:
def startMission():
    max_retries = 3
    for retry in range(max_retries):
        try:
            agent_host.startMission(my_mission, my_mission_record)
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print("Error starting mission:", e)
                exit(1)
            else:
                time.sleep(2)

# Loop until mission starts:


def waitUntilMissionStart():
    print("Waiting for the mission to start ", end=' ')
    world_state = agent_host.getWorldState()
    while not world_state.has_mission_begun:
        print(".", end="")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:", error.text)

    print()
    print("Mission running ", end=' ')


def missionLoop():
    world_state = agent_host.getWorldState()
    my_agent = MyAgent(world_state)
    i = 0
    while world_state.is_mission_running:
        time.sleep(0.2)
        world_state = agent_host.getWorldState()
        my_agent.updateWorldState(world_state)
        action = my_agent.takeAction()
        if action:
            print(action)
            agent_host.sendCommand(action)
        for error in world_state.errors:
            print("Error:", error.text)
    print()
    print("Mission ended")
# Mission has ended.


hello = "hello"
if __name__ == "__main__":
    setupMission()
    startMission()
    waitUntilMissionStart()
    missionLoop()
