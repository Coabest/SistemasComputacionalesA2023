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
        self.rows = self.game.world.tile_map.rows
        self.cols = self.game.world.tile_map.cols
        self.n = (self.rows * self.cols)
        self.observation_space = spaces.Discrete(self.n * self.n * self.n)
        self.action_space = spaces.Discrete(4)
        self.states_n = self.n * self.n * self.n
        self.actions_n = 4
        self.current_state = self.game.get_state()
        self.current_action = 0
        self.reward = 0.0
        self.terminated = False
        self.delay = 1
        
        self.P = self.__build_P()
        
    def __build_P(self):

        P = { state: { action: [] for action in range(self.actions_n) } for state in range(self.states_n) }

        for state in range(self.states_n):
            for action in range(self.actions_n):
                probability = 1.0
                next_state = 0
                reward = -5.0
                self.terminated = False

                # set the game state back !!!
                individual_states = self.__compute_individual_states(state)
                mc, s1, s2 = individual_states
                self.game.world.set_state(mc, s1, s2)

                # Check some invalid states and skip
                if ((s1 == s2)
                    or ((mc, s1, s2) == 2)
                    or ((mc, s1, s2) == 15)
                    or ((mc, s1, s2) == 19)
                    or ((mc, s1, s2) == 20)
                    or ((mc, s1, s2) == 24)
                    or ((mc, s1, s2) == 25)
                    or ((mc, s1, s2) == 26)
                    or ((mc, s1, s2) == 28)
                    or ((mc, s1, s2) == 29)):
                    continue

                # Check if it is in a win state, i.e. 188 or 246
                if (self.game.world.check_win()):
                    P[state][action].append([1.0, state, 0.0, False])
                    continue
                
                # Calculate next state
                next_state_tuple = self.game.world.apply_action(action)
                next_state = self.__compute_state_result(*next_state_tuple)

                # Determine reward
                if state == next_state:
                    reward = -50.0
                elif self.game.world.check_lost():
                    reward = -500.0
                    self.terminated = True
                elif self.game.world.check_win():
                    reward = 1000.0
                    self.terminated = True

                P[state][action].append([probability, next_state, reward, self.terminated])
                # time.sleep(1)

        self.current_state = self.game.reset()
        return P

    def __compute_state_result(self, mc, s1, s2):
        return int(mc * self.n**2 + s1 * self.n + s2)

    def __compute_individual_states(self, state):
        s2 = int(state % self.n); state = int(state / self.n)
        s1 = int(state % self.n); state = int(state / self.n)
        mc = int(state % self.n)
        
        return mc, s1, s2
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        if options is not None:
            if not isinstance(options, dict):
                raise RuntimeError("Variable options is not a dictionary")
            self.delay = options.get("delay", 0.5)

        np.random.seed(seed)

        self.current_state = self.game.reset()
        self.current_action = 0
        self.reward = 0

        return self.__compute_state_result(*self.current_state), {}

    def step(self, action):
        print("state {} action {} reward {} terminated {} >>> ".format
        (
            self.current_state,
            action,
            self.reward,
            self.terminated
        ), end="")
        self.current_action = action
        state = self.__compute_state_result(*self.current_state)
        self.reward = self.P[state][action][0][2]
        self.terminated = self.P[state][action][0][3]
        self.current_state = self.__compute_individual_states(self.P[state][action][0][1])

        self.game.world.set_state(*self.current_state)

        if self.render_mode is not None:
            self.render()
            time.sleep(self.delay)

        print(self.current_state)

        return (
            self.__compute_state_result(*self.current_state),
            self.reward,
            self.terminated,
            False,
            {}
        )

    def render(self):
        self.game.render()

    def close(self):
        self.game.close()
