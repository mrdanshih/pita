from __future__ import print_function
import os
import sys
import time
import datetime
import json
import random
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.layers.advanced_activations import PReLU

visited_mark = 0.8  # Cells visited by the rat will be painted by gray 0.8
rat_mark = 0.5      # The current rat cell will be painteg by gray 0.5
LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

# Actions dictionary

# up down right left
actions = [0, 1, 2, 3]

num_actions = len(actions)

# Exploration factor
epsilon = 0.1


class Experience(object):
    def __init__(self, model, max_memory=100, discount=0.95):
        self.model = model
        self.max_memory = max_memory
        self.discount = discount
        self.memory = list()
        self.num_actions = model.output_shape[-1]

    def remember(self, episode):
        # episode = [envstate, action, reward, envstate_next, game_over]
        # memory[i] = episode
        # envstate == flattened 1d maze cells info, including rat cell (see method: observe)
        self.memory.append(episode)
        if len(self.memory) > self.max_memory:
            del self.memory[0]

    def predict(self, envstate):
        if (envstate.ndim == 1):
            envstate = np.array([envstate])
        return self.model.predict(envstate)[0]

    def get_data(self, data_size=10):
        # envstate 1d size (1st element of episode)
        env_size = self.memory[0][0].size
        mem_size = len(self.memory)
        data_size = min(mem_size, data_size)
        inputs = np.zeros((data_size, env_size))
        targets = np.zeros((data_size, self.num_actions))
        for i, j in enumerate(np.random.choice(range(mem_size), data_size, replace=False)):
            envstate, action, reward, envstate_next, game_over = self.memory[j]
            inputs[i] = envstate
            # There should be no target values for actions not taken.
            targets[i] = self.predict(envstate)
            # Q_sa = derived policy = max quality env/action = max_a' Q(s', a')
            Q_sa = np.max(self.predict(envstate_next))
            if game_over:
                targets[i, action] = reward
            else:
                # reward + gamma * max_a' Q(s', a')
                targets[i, action] = reward + self.discount * Q_sa
        return inputs, targets


def build_model(world, lr=0.001):
    model = Sequential()
    model.add(Dense(world.size, input_shape=(world.size,)))
    model.add(PReLU())
    model.add(Dense(world.size))
    model.add(PReLU())
    model.add(Dense(world.size))
    model.add(PReLU())
    model.add(Dense(num_actions))
    model.compile(optimizer='adam', loss='mse')
    return model


class World:
    def __init__(self):
        self.world = self.reset()

    def reset(self):
        world = np.zeros((10, 10))
        world[0][0] = 1
        world[0][9] = 2
        world[9][9] = 2
        world[9][0] = 2
        self.state = (0, 0, 'start')
        self.total_reward = 0
        self.total_steps = 30
        self.world = world
        return world

    def update_state(self, action):
        nrows, ncols = self.world.shape
        nrow, ncol, nmode = self.state
        self.world[nrow][ncol] = 0
        nmode = "invalid"
        if ncol < ncols-1 and action == 2:
            ncol += 1
            nmode = "valid"
        elif ncol > 0 and action == 3:
            ncol -= 1
            nmode = "valid"
        elif nrow < nrows - 1 and action == 1:
            nrow += 1
            nmode = "valid"
        elif nrow > 0 and action == 0:
            nrow -= 1
            nmode = "valid"
        self.world[nrow][ncol] = 1
        self.state = (nrow, ncol, nmode)
        #print(self.state, end=", ")

    def get_reward(self):
        nrows, ncols = self.world.shape
        row, col, mode = self.state
        for i in range(nrows):
            for j in range(ncols):
                if (self.world[i][j] == 2):
                    dist = abs(i - row)**2 + abs(j-col)**2
                    if dist <= 4:
                        self.world[i][j] = 0
                        return 100

        if mode == 'invalid':
            return -2
        if mode == 'valid':
            return -1

    def game_status(self):
        nrows, ncols = self.world.shape
        sheepLeft = 0
        for i in range(nrows):
            for j in range(ncols):
                if self.world[i][j] == 2:
                    sheepLeft += 1

        if self.total_steps > 0 and sheepLeft > 0:
            return "not over"
        elif self.total_reward < 0:
            return "lose"
        else:
            return "win"

    def observe(self):
        return self.world.reshape(-1)

    def act(self, action):
        # print("Action taken: " + str(action), end=", ")
        self.total_steps -= 1
        self.update_state(action)
        reward = self.get_reward()
        self.total_reward += reward
        # print("Reward: " + str(self.total_reward))
        envstate = self.observe()
        status = self.game_status()
        return envstate, reward, status


def format_time(seconds):
    if seconds < 400:
        s = float(seconds)
        return "%.1f seconds" % (s,)
    elif seconds < 4000:
        m = seconds / 60.0
        return "%.2f minutes" % (m,)
    else:
        h = seconds / 3600.0
        return "%.2f hours" % (h,)


def qtrain(model, world):
    n_epoch = 15000
    max_memory = 1000
    data_size = 50

    experience = Experience(model, max_memory=max_memory)
    win_history = []
    win_rate = 0.0
    epsilon = 0.15
    hsize = world.world.size // 4
    print(hsize)
    start_time = datetime.datetime.now()
    for epoch in range(n_epoch):
        loss = 0.0
        envstate = world.observe()
        n_episodes = 0
        world.reset()
        game_over = False

        while not game_over:
            prev_envstate = envstate
            if np.random.rand() < epsilon:
                action = random.choice(actions)
            else:
                action = np.argmax(experience.predict(prev_envstate))
            envstate, reward, game_status = world.act(action)
            if game_status == 'win':
                win_history.append(1)
                game_over = True
            elif game_status == 'lose':
                win_history.append(0)
                game_over = True
            else:
                game_over = False
            episode = [prev_envstate, action, reward, envstate, game_over]
            experience.remember(episode)
            n_episodes += 1
            inputs, targets = experience.get_data(data_size=data_size)
            h = model.fit(
                inputs,
                targets,
                epochs=8,
                batch_size=16,
                verbose=0,
            )
            loss = model.evaluate(inputs, targets, verbose=0)
        if len(win_history) > hsize:
            win_rate = sum(win_history[-hsize:]) / hsize

        dt = datetime.datetime.now() - start_time
        t = format_time(dt.total_seconds())
        template = "Epoch: {:03d}/{:d} | Loss: {:.4f} | Episodes: {:d} | Win count: {:d} | Win rate: {:.3f} | time: {}"
        print(template.format(epoch, n_epoch-1, loss,
                              n_episodes, sum(win_history), win_rate, t))
        # we simply check if training has exhausted all free cells and if in all
        # cases the agent won
        if win_rate > 0.9:
            epsilon = 0.05
        if sum(win_history[-hsize:]) == hsize and completion_check(model, qmaze):
            print("Reached 100%% win rate at epoch: %d" % (epoch,))
            break
    h5file = "model" + ".h5"
    json_file = "model" + ".json"
    model.save_weights(h5file, overwrite=True)
    with open(json_file, "w") as outfile:
        json.dump(model.to_json(), outfile)
    end_time = datetime.datetime.now()
    dt = datetime.datetime.now() - start_time
    seconds = dt.total_seconds()
    t = format_time(seconds)
    print('files: %s, %s' % (h5file, json_file))
    print("n_epoch: %d, max_mem: %d, data: %d, time: %s" %
          (epoch, max_memory, data_size, t))


if __name__ == "__main__":
    world = World()
    model = build_model(world.world)
    qtrain(model, world)
