import numpy as np

class TwoArmedBandit():
    def __init__(self, alpha=1):
        self.arms = 2
        self.alpha = alpha
        self.reset()

    def reset(self):
        self.action = 0
        self.reward = 0
        self.iteration = 0
        self.values = np.zeros(self.arms)
        self.totalReward = 0
        self.epsilon = 0.9


    def update(self, action, reward):
        self.action = action
        self.reward = reward
        self.iteration += 1
        self.values[action] = self.values[action] + self.alpha * (reward - self.values[action])
        self.totalReward += self.reward

    def get_action(self, mode):

        if mode == 'random':
            return np.random.choice(self.arms)
        elif mode == 'greedy':
            return np.argmax(self.values)
        elif mode == 'eps_greedy':
            if np.random.sample(1) < self.epsilon:
                return np.random.choice(self.arms)
            else:
                return np.argmax(self.values)

    def render(self):
        print("Iteration: {}, Action: {}, Reward: {}, Values: {}".format(
            self.iteration, self.action, self.reward, self.values))
        
