import time

import numpy as np

import pygame

import gym
from gym import spaces

from .game.Game import Game


class PrincessEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, **kwargs):
        super().__init__()
        self.render_mode = kwargs.get("render_mode")
        self.game = Game("Princess Puzzle Env", self.render_mode)
        self.n = self.game.world.tile_map.rows * self.game.world.tile_map.cols
        self.observation_space = spaces.Discrete(self.n * self.n * self.n)
        self.action_space = spaces.Discrete(4)
        self.current_state = self.game.get_state()
        self.current_action = 0
        self.current_reward = 0.0
        self.delay = 1

    def __compute_state_result(self, mc, s1, s2):
        return mc * self.n**2 + s1 * self.n + s2

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        if options is not None:
            if not isinstance(options, dict):
                raise RuntimeError("Variable options is not a dictionary")
            self.delay = options.get("delay", 0.5)

        np.random.seed(seed)

        self.current_state = self.game.reset()
        self.current_action = 0
        self.current_reward = 0

        return self.__compute_state_result(*self.current_state), {}

    def step(self, action):
        self.current_action = action

        old_state = self.current_state
        self.current_state = self.game.update(self.current_action)

        terminated = False
        self.current_reward = -1.0

        if old_state == self.current_state:
            self.current_reward = -10.0
        elif self.game.world.check_lost():
            terminated = True
            self.current_reward = -100.0
        elif self.game.world.check_win():
            terminated = True
            self.current_reward = 1000.0

        if self.render_mode is not None:
            self.render()
            time.sleep(self.delay)

        return (
            self.__compute_state_result(*self.current_state),
            self.current_reward,
            terminated,
            False,
            {},
        )

    def render(self):
        self.game.render()

    def close(self):
        self.game.close()
