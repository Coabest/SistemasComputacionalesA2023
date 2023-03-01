import sys
import time
import gym
import gym_environments
from agent import DoubleQLearning, QLearning

import matplotlib.pyplot as plt
import numpy as np


def train(env, agent, episodes):
    table = []

    for episode in range(episodes):
        y = 0

        observation, _ = env.reset()
        terminated, truncated = False, False
        while not (terminated or truncated):
            action = agent.get_action(observation, "epsilon-greedy")
            new_observation, reward, terminated, truncated, _ = env.step(action)
            y += reward
            agent.update(observation, action, new_observation, reward, terminated)
            observation = new_observation
        table.append(y)
    
    return table

def play(env, agent):
    observation, _ = env.reset()
    terminated, truncated = False, False

    env.render()
    time.sleep(1)

    while not (terminated or truncated):
        action = agent.get_action(observation, "greedy")
        new_observation, reward, terminated, truncated, _ = env.step(action)
        agent.update(observation, action, new_observation, reward, terminated)
        observation = new_observation


if __name__ == "__main__":
    environments = ["CliffWalking-v0", "Taxi-v3", "Princess-v0", "Blocks-v0"]
    id = 0 if len(sys.argv) < 2 else int(sys.argv[1])
    episodes = 10000 if len(sys.argv) < 3 else int(sys.argv[2])

    env = gym.make(environments[id])

    Q_rewards  = np.zeros(episodes)
    QQ_rewards = np.zeros(episodes)
    tests = 500

    for i in range(tests):
        Q_agent = QLearning(
            env.observation_space.n, env.action_space.n, alpha=0.1, gamma=0.9, epsilon=0.3
        )
        QQ_agent = DoubleQLearning(
            env.observation_space.n, env.action_space.n, alpha=0.1, gamma=0.9, epsilon=0.3
        )
        if (i%(int(tests/10 + 1))==0):
            print("test #{}".format(i))
        Q_table  = train(env,  Q_agent, episodes)
        QQ_table = train(env, QQ_agent, episodes)
        for episode in range(episodes):
            Q_rewards[episode]  += Q_table[episode]
            QQ_rewards[episode] += QQ_table[episode]

    for episode in range(episodes):
        Q_rewards[episode]  /= tests
        QQ_rewards[episode] /= tests

    plt.plot(Q_rewards, label = 'QLearning')
    plt.plot(QQ_rewards, label = 'QQLearning')
    plt.xlabel('x - Episode')
    plt.ylabel('y - Reward')
    
    plt.title('QLearning Vs. Double QLearning')
    plt.legend()
    plt.show()

    QQ_agent.render()
    env.close()
