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
        self.action_space = gym.spaces.Discrete(settingss.NUM_ACTIONS)
        self.observation_space = gym.spaces.Discrete(settingss.NUM_TILES)
        self.current_action = 1
        self.current_state = 0
        self.current_reward = 0.0
        self.delay = settingss.DEFAULT_DELAY
        self.battery = settingss.BATTERY

        self.P = { state: { action: [] for action in range(settingss.NUM_ACTIONS) } for state in range(settingss.NUM_TILES) }

        # for row in range(settingss.ROWS):
        #     for col in range(settingss.COLS):
            
        for state in range(settingss.NUM_TILES):
            for action in range(settingss.NUM_ACTIONS):
                probability = 1.0
                next_state = state
                reward = float(state == settingss.FINAL_STATE)
                
                # Calculate next state
                row = int(state / settingss.ROWS)
                col = int(state % settingss.COLS)
                if action == 0:
                    next_state = state if col == 0 else row * settingss.ROWS + col - 1
                elif action == 1:
                    next_state = state if row == settingss.ROWS - 1 else (row + 1) * settingss.ROWS + col
                elif action == 2:
                    next_state = state if col == settingss.COLS - 1 else row * settingss.ROWS + col + 1
                elif action == 3:
                    next_state = state if row == 0 else (row - 1) * settingss.ROWS + col

                if state == settingss.FINAL_STATE:
                    next_state = state

                truncated = next_state == settingss.FINAL_STATE
                # print ("getting to {} from {}, with action {}".format(next_state, state, action))
                self.P[state][action].append([probability, next_state, reward, truncated])

        # Action(n) = [probability, next_state, reward, truncated]        

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
        self.state = settingss.INITIAL_STATE
        self.battery = settingss.BATTERY
        self.world.reset(self.state, self.action)
        return self.state, {}

    def step(self, action):
        self.battery -= 1
        self.action = self.current_action = action
        
        rng = np.random.random()
        print ("is {} < {}?".format(rng, 1.0 - self.battery / settingss.BATTERY))
        
        if  rng < 1 - self.battery / settingss.BATTERY:
            # Elegir ir a una diferente a la elegida por la acción
            print ("Wrong action chosen!")
            self.action = self.current_action = (action + 1)%settingss.NUM_ACTIONS
        
        self.reward = self.current_reward = self.P[self.current_state][action][0][2]
        terminated = self.P[self.current_state][action][0][3] if self.battery else True
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
        # print(self.battery)
        self.world.render()
        # print(
        #     "Action {}, reward {}, state {}".format(
        #         self.action,
        #         self.reward,
        #         self.state))
