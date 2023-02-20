import time

import numpy as np

import gym
from gym import spaces
import pygame

from . import settings
from .world import World


class FrozenLakeEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, **kwargs):
        super().__init__()
        self.observation_space = spaces.Discrete(settings.NUM_TILES)
        self.action_space = spaces.Discrete(settings.NUM_ACTIONS)
        self.current_action = 1
        self.current_state = 0
        self.current_reward = 0.0
        self.delay = settings.DEFAULT_DELAY

        self.P = { state: { action: [] for action in range(settings.NUM_ACTIONS) } for state in range(settings.NUM_TILES) }
        
        for state in range(settings.NUM_TILES):
            for action in range(settings.NUM_ACTIONS):
                if (state == settings.FINAL_STATE):
                    self.P[state][action].append([1.0, state, 0.0, True])
                    continue

                probability = 1.0
                next_state = 0
                reward = 0.0
                truncated = False
                
                # Calculate next state
                row = int(state / settings.ROWS)
                col = int(state % settings.COLS)
                if action == 0:
                    next_state = state if col == 0 else row * settings.COLS + col - 1
                    if next_state == settings.FINAL_STATE:
                        print("reward assigned at state {}".format(state))
                        reward = 1.0

                    self.P[state][action].append([probability, next_state, reward, truncated]) 

                elif action == 1:
                    next_state = state if row == settings.ROWS - 1 else (row + 1) * settings.COLS + col
                    if next_state == settings.FINAL_STATE:
                        print("reward assigned at state {}".format(state))
                        reward = 1.0

                    self.P[state][action].append([probability, next_state, reward, truncated]) 
                elif action == 2:
                    next_state = state if col == settings.COLS - 1 else row * settings.COLS + col + 1
                    if next_state == settings.FINAL_STATE:
                        print("reward assigned at state {}".format(state))
                        reward = 1.0

                    self.P[state][action].append([probability, next_state, reward, truncated]) 
                elif action == 3:
                    next_state = state if row == 0 else (row - 1) * settings.COLS + col
                    if next_state == settings.FINAL_STATE:
                        print("reward assigned at state {}".format(state))
                        reward = 1.0

                    self.P[state][action].append([probability, next_state, reward, truncated]) 

                

        self.world = World(
            "Frozen Lake Environment", self.current_state, self.current_action
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        if options is not None:
            if not isinstance(options, dict):
                raise RuntimeError("Variable options is not a dictionary")
            self.delay = options.get("delay", 0.5)

        np.random.seed(seed)
        self.current_state = 0
        self.current_action = 1
        self.world.reset(self.current_state, self.current_action)
        return 0, {}

    def step(self, action):
        self.current_action = action

        possibilities = self.P[self.current_state][self.current_action]

        p = 0
        i = 0

        r = np.random.random()
        while r > p:
            r -= p
            p, self.current_state, self.current_reward, terminated = possibilities[i]
            i += 1

        self.world.update(
            self.current_state, self.current_action, self.current_reward, terminated
        )

        self.render()
        time.sleep(self.delay)

        return self.current_state, self.current_reward, terminated, False, {}

    def render(self):
        self.world.render()

    def close(self):
        self.world.close()
