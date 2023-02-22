# V023723245 Lezama Luis
# V025793252 Ramírez Coalbert

import numpy as np


class QLearning:
    def __init__(self, states_n, actions_n, alpha, gamma, epsilon):
        self.states_n = states_n
        self.actions_n = actions_n
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.reset()

    def reset(self):
        self.episode = 0
        self.iteration = 0
        self.state = 0
        self.action = 0
        self.next_state = 0
        self.reward = 0
        self.q_table = np.zeros((self.states_n, self.actions_n))

    def update(self, current_state, action, next_state, reward, terminated):
        self._update(current_state, action, next_state, reward, terminated)
        self.q_table[current_state, action] = self.q_table[
            current_state, action
        ] + self.alpha * (
            reward
            + self.gamma * np.max(self.q_table[next_state])
            - self.q_table[current_state, action]
        )

    def _update(self, current_state, action, next_state, reward, terminated):
        self.iteration += 1
        self.state = current_state
        self.action = action
        self.next_state = next_state
        self.reward = reward
        if terminated:
            self.episode += 1
            self.iteration = 0

    def get_action(self, state, mode):
        if mode == "random":
            return np.random.choice(self.actions_n)
        elif mode == "greedy":
            return np.argmax(self.q_table[state])
        elif mode == "epsilon-greedy":
            rdm = np.random.uniform(0, 1)
            if rdm < self.epsilon:
                return np.random.choice(self.actions_n)
            else:
                return np.argmax(self.q_table[state])

    def render(self, mode="values"):
        if mode == "step":
            print(
                "Episode: {}, Iteration: {}, State: {}, Action: {}, Next state: {}, Reward: {}".format(
                    self.episode,
                    self.iteration,
                    self.state,
                    self.action,
                    self.next_state,
                    self.reward,
                )
            )
        elif mode == "values":
            print("Q-Table: {}".format(self.q_table))

class ValueIteration():
    def __init__(self, states_n, actions_n, P, gamma):
        self.states_n = states_n
        self.actions_n = actions_n
        self.P = P
        self.gamma = gamma
        self.reset()

    def reset(self):
        self.values = np.zeros(self.states_n)
        self.policy = np.zeros(self.states_n)

    def get_action(self, state):
        return int(self.policy[state])

    def render(self):
        print("Values: {}, Policy: {}".format(self.values, self.policy))

    def solve(self, iterations):
        for i in range(iterations):
            for s in range(self.states_n):
                values = [sum([prob * (r + self.gamma * self.values[s_])
                               for prob, s_, r, _ in self.P[s][a]])
                          for a in range(self.actions_n)]
                self.values[s] = max(values)
                self.policy[s] = np.argmax(np.array(values))
