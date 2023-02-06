import time

import numpy as np

import gym
from gym import spaces
import pygame

from . import settingss
from .world import World

class RobotBatteryEnv(gym.Env):

    metadata = {"render_modes": ["human"], "render_fps": 16}

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
                if (state == settingss.FINAL_STATE):
                    self.P[state][action].append([1.0, state, 1.0, True])
                    print("assigned reward at state {}".format(state))
                    break

                probability = 1.0
                next_state = 0
                reward = 0.0
                
                
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

                if next_state == settingss.FINAL_STATE:
                    reward = 1.0

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
        self.current_action = 0
        self.current_reward = 0.0
        self.current_state = settingss.INITIAL_STATE
        self.battery = settingss.BATTERY
        # self.world.reset(self.state, self.action)
        return self.current_state, {}

    def step(self, action):
        self.battery = max(0, self.battery - settingss.BATTERY_DISCOUNT)
        self.current_action = action

        print("in state {} should go to {} with action {}".format(self.current_state, self.P[self.current_state][action][0][1], action), end="")

        rng = np.random.random()
        # print ("is {} < {}?".format(rng, 1.0 - self.battery / settingss.BATTERY))
        
        if  rng < 1 - self.battery / settingss.BATTERY:
            # Elegir ir a una diferente a la elegida por la acción
            print (" BUT Wrong action chosen!", end="")
            # Calculate next state
            row = int(self.current_state / settingss.ROWS)
            col = int(self.current_state % settingss.COLS)

            next_action = np.random.randint(0, settingss.NUM_ACTIONS)
            while next_action == action:
                next_action = np.random.randint(0, settingss.NUM_ACTIONS)
            
            # if next_action == 0:
            #     col = col if col == 0 else col - 1
            # if next_action == 1:
            #     row = row if row < settingss.ROWS - 1 else row + 1
            # if next_action == 2:
            #     col = col if col < settingss.COLS - 1 else col + 1
            # if next_action == 3:
            #     row = row if row == 0 else row - 1

            self.current_action = next_action
            # self.current_state = row * settingss.ROWS + col
            
        print(" and got to state {} with action {} and {} battery".format(self.P[self.current_state][self.current_action][0][1], self.current_action, self.battery))
        self.reward = self.current_reward = self.P[self.current_state][self.current_action][0][2]
        terminated = self.P[self.current_state][self.current_action][0][3] if self.battery > 0 else True
        self.state = self.current_state = self.P[self.current_state][self.current_action][0][1]     

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
        # print("batery at {}%".format(self.battery))
        self.world.render()
        print(
            "Action {}, reward {}, state {}".format(
                self.current_action,
                self.current_reward,
                self.current_state))
