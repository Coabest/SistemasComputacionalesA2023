import numpy as np
import gym


class TwoArmedBanditEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = gym.spaces.Discrete(2)
        self.observation_space = gym.spaces.Discrete(1)
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.action = 0
        self.reward = 0
        return 0, {}

    def step(self, action):
        assert self.action_space.contains(action)
        self.action = action
        if self.action == 0:
            self.reward = np.random.choice(2, p=[0.5, 0.5])
        elif self.action == 1:
            self.reward = 100 * np.random.choice(2, p=[0.9, 0.1])
        return 0, self.reward, False, False, {}

    def render(self, mode="human", close=False):
        print("Action {}, reward {}".format(self.action, self.reward))
