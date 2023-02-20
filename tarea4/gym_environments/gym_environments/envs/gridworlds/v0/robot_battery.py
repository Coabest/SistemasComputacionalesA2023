import time

import numpy as np

import gym
from gym import spaces
import pygame

from . import settingss
from .world import World

class RobotBatteryEnv(gym.Env):

    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, render_mode=None):
        super().__init__()
        self.action_space = gym.spaces.Discrete(settingss.NUM_ACTIONS)
        self.observation_space = gym.spaces.Discrete(settingss.NUM_TILES)
        self.action = 1
        self.state = 0
        self.reward = 0.0
        self.delay = settingss.DEFAULT_DELAY
        self.battery = settingss.BATTERY

        self.P = { state: { action: [] for action in range(settingss.NUM_ACTIONS) } for state in range(settingss.NUM_TILES) }

        for state in range(settingss.NUM_TILES):
            for action in range(settingss.NUM_ACTIONS):
                if (state == settingss.FINAL_STATE):
                    self.P[state][action].append([1.0, state, 0.0, True])
                    continue

                probability = 1.0
                next_state = 0
                reward = 0.0
                
                # Calculate next state
                row = int(state / settingss.ROWS)
                col = int(state % settingss.COLS)
                if action == 0:
                    next_state = state if col == 0 else row * settingss.COLS + col - 1
                elif action == 1:
                    next_state = state if row == settingss.ROWS - 1 else (row + 1) * settingss.COLS + col
                elif action == 2:
                    next_state = state if col == settingss.COLS - 1 else row * settingss.COLS + col + 1
                elif action == 3:
                    next_state = state if row == 0 else (row - 1) * settingss.COLS + col

                if next_state == settingss.FINAL_STATE:
                    reward = 1.0

                truncated = False
                self.P[state][action].append([probability, next_state, reward, truncated])     

        self.reset()
        self.world = World(
            "Robot Battery Environment",
            self.state,
            self.action,
            self.P,
            self.battery
        )


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.action = 0
        self.reward = 0.0
        self.state = settingss.INITIAL_STATE
        self.battery = settingss.BATTERY
        # self.world.reset(self.state, self.action)
        return self.state, {}

    def step(self, action):
        self.battery = max(0, self.battery - settingss.BATTERY_DISCOUNT)
        self.action = action

        rng = np.random.random()
        if  rng < 1 - self.battery / settingss.BATTERY:
            # Choose a wrong action
            wrong_action = np.random.randint(0, settingss.NUM_ACTIONS)
            while wrong_action == action:
                wrong_action = np.random.randint(0, settingss.NUM_ACTIONS)
            self.action = wrong_action

        self.state = self.P[self.state][self.action][0][1]
        self.reward = self.P[self.state][self.action][0][2]
        terminated = self.P[self.state][self.action][0][3] if self.battery > 0 else True
        
        self.world.update(
            self.battery,
            self.state,
            self.action,
            self.reward,
            terminated
        )
        
        self.render()
        time.sleep(settingss.DEFAULT_DELAY)
        return self.state, self.reward, terminated, False, {}

    def render(self):
        self.world.render()
        # print(
        #     "Action {}, reward {}, state {}".format(
        #         self.action,
        #         self.reward,
        #         self.state))
