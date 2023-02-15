import time

import numpy as np

import gym
from gym import spaces

from .game.Game import Game


class BlocksEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, **kwargs):
        super().__init__()
        self.render_mode = kwargs.get("render_mode")
        self.game = Game("Blocks Puzzle Env", self.render_mode)
        self.n = self.game.scene.tile_map.rows * self.game.scene.tile_map.cols
        self.num_directions = 4
        self.observation_space = spaces.Discrete(
            self.n * (self.n - 1) * (self.n - 2) * self.num_directions
        )
        self.action_space = spaces.Discrete(5)
        self.current_state = self.game.get_state()
        self.current_action = 0
        self.current_reward = 0.0
        self.delay = 1

    def __compute_state_result(self, d, mc, s1, s2):
        return (
            d * self.n * (self.n - 1) * (self.n - 2)
            + mc * (self.n - 1) * (self.n - 2)
            + s1 * (self.n - 2)
            + s2
        )

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
        self.current_state, terminated = self.game.update(self.current_action)

        self.current_reward = -1.0

        if old_state == self.current_state:
            self.current_reward = -10.0
        elif terminated:
            self.current_reward = 0

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
