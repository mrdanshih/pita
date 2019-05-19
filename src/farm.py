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
from farmworld import World
from myagent import Experience
from enum import Enum
import MalmoPython
import os
import sys
import time
import math
import random
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.layers.advanced_activations import PReLU


def build_model(world, lr=0.001):
    model = Sequential()
    model.add(Dense(world.size, input_shape=(world.size,)))
    model.add(PReLU())
    model.add(Dense(world.size))
    model.add(PReLU())
    model.add(Dense(world.size))
    model.add(PReLU())
    model.add(Dense(4))
    model.compile(optimizer='adam', loss='mse')
    return model


if __name__ == "__main__":
    world = World()
    model = build_model(world.world)
    max_memory = 1000
    data_size = 50
    experience = Experience(model, max_memory=max_memory)
    agent_host = MalmoPython.AgentHost()
    # -- set up the mission -- #
    mission_file = './farm.xml'
    with open(mission_file, 'r') as f:
        print("Loading mission from %s" % mission_file)
        mission_xml = f.read()
        my_mission = MalmoPython.MissionSpec(mission_xml, True)

    max_retries = 3
    num_repeats = 150
    for i in range(num_repeats):
        world.reset()
        envstate = world.observe()

        print()
        print('Repeat %d of %d' % (i+1, num_repeats))

        my_mission_record = MalmoPython.MissionRecordSpec()
        for retry in range(max_retries):
            try:
                agent_host.startMission(my_mission, my_mission_record)
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission:", e)
                    exit(1)
                else:
                    time.sleep(2.5)

        print("Waiting for the mission to start", end=' ')
        world_state = agent_host.getWorldState()
        while not world_state.has_mission_begun:
            print(".", end="")
            time.sleep(0.1)
            world_state = agent_host.getWorldState()
            for error in world_state.errors:
                print("Error:", error.text)
        print()

        # -- run the agent in the world -- #
        while world_state.is_mission_running:
            time.sleep(0.1)
            prev_envstate = envstate

            if np.random.rand() < 0.1:
                action = random.choice(world.actions)
            else:
                action = np.argmax(experience.predict(prev_envstate))
            print(world.actionMap[action], end=": ")
            agent_host.sendCommand(world.actionMap[action])
            world_state = agent_host.getWorldState()
            envstate, reward, game_status = world.update_state(world_state)
            print(reward, game_status)
            game_over = game_status == 'win' or game_status == 'lose'
            episode = [prev_envstate, action, reward, envstate, game_over]
            experience.remember(episode)
            inputs, targets = experience.get_data(data_size=data_size)
            h = model.fit(
                inputs,
                targets,
                epochs=8,
                batch_size=16,
                verbose=0,
            )
            loss = model.evaluate(inputs, targets, verbose=0)
            if game_over:
                agent_host.sendCommand("quit")
                break
        # -- clean up -- #
        time.sleep(0.5)  # (let the Mod reset)
    h5file = "model" + ".h5"
    json_file = "model" + ".json"
    model.save_weights(h5file, overwrite=True)
    with open(json_file, "w") as outfile:
        json.dump(model.to_json(), outfile)

    print("Done.")
