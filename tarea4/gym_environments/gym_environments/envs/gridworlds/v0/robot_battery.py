import time

import numpy as np

import gym
from gym import spaces
import pygame

from . import settingss
from .world import World

class RobotBatteryEnv(gym.Env):

    def __init__(self, render_mode=None):
        super().__init__()
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Discrete(6)
        self.current_action = 1
        self.current_state = 0
        self.current_reward = 0.0
        self.delay = settingss.DEFAULT_DELAY
        self.battery = settingss.BATTERY
        self.P = {0: {0: [(1, 0, 0.0, False)], 1: [(1, 2, 0.0, False)], 2: [(1, 1, 0.0, False)], 3: [(1, 0, 0.0, False)]},
                  1: {0: [(1, 0, 0.0, False)], 1: [(1, 3, 0.0, False)], 2: [(1, 1, 0.0, False)], 3: [(1, 1, 0.0, False)]},
                  2: {0: [(1, 2, 0.0, False)], 1: [(1, 4, 0.0, False)], 2: [(1, 3, 0.0, False)], 3: [(1, 0, 0.0, False)]},
                  3: {0: [(1, 2, 0.0, False)], 1: [(1, 5, 1.0,  True)], 2: [(1, 3, 0.0, False)], 3: [(1, 1, 0.0, False)]},
                  4: {0: [(1, 4, 0.0, False)], 1: [(1, 4, 0.0, False)], 2: [(1, 5, 1.0,  True)], 3: [(1, 2, 0.0, False)]},
                  5: {0: [(1, 5, 0.0,  True)], 1: [(1, 5, 0.0,  True)], 2: [(1, 5, 0.0,  True)], 3: [(1, 5, 0.0,  True)]}}
        self.reset()
        self.world = World(
            "Robot Battery Environment",
            self.current_state,
            self.current_action,
            self.P,
            self.battery
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.action = 0
        self.reward = 0.0
        self.state = 0
        return self.state, {}

    def step(self, action):
        self.battery -= 1
        self.action = self.current_action = action

        if np.random.random() < 1 - self.battery / settingss.BATTERY:
            # Elegir ir a una diferente a la elegida por la acción
            self.action = self.current_action = (action + 1)%settingss.NUM_ACTIONS
        
        self.reward = self.current_reward = self.P[self.current_state][action][0][2]
        terminated = self.P[self.current_state][action][0][3]
        self.state = self.current_state = self.P[self.current_state][action][0][1]        

        self.world.update(
            self.current_state,
            self.current_action,
            self.current_reward,
            terminated
        )
        
        self.render()
        time.sleep(0.25)
        return self.state, self.reward, terminated, False, {}

    def render(self):
        self.world.render()
        print(
            "Action {}, reward {}, state {}".format(
                self.action,
                self.reward,
                self.state))
