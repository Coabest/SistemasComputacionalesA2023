import sys
import gym
import gym_environments
from agent import SARSA

import matplotlib.pyplot as plt
import numpy as np
from statistics import mean


def calculate_states_size(env):
    max = env.observation_space.high
    min = env.observation_space.low
    sizes = (max - min) * np.array([10, 100]) + 1
    return int(sizes[0]) * int(sizes[1])


def calculate_state(env, value):
    min = env.observation_space.low
    values = (value - min) * np.array([10, 100])
    return int(values[1]) * 19 + int(values[0])


def run(env, agent, selection_method, episodes, algorithm):
    table = []
    for episode in range(1, episodes + 1):
        y = 0
        if episode % 500 == 0:
            print(f"   {algorithm}, Episode: {episode}")
        observation, _ = env.reset()
        action = agent.get_action(calculate_state(env, observation), selection_method)
        terminated, truncated = False, False
        while not (terminated or truncated):
            new_observation, reward, terminated, truncated, _ = env.step(action)
            y += reward
            next_action = agent.get_action(
                calculate_state(env, new_observation), selection_method
            )
            agent.update(
                calculate_state(env, observation),
                action,
                calculate_state(env, new_observation),
                next_action,
                reward,
                terminated,
                truncated,
                algorithm
            )
            observation = new_observation
            action = next_action
        table.append(y)
        # print(f"     On episode {episode}, reward is {y}")
    # average value of rewards
    return mean(table)
    # return table[-1]


if __name__ == "__main__":
    episodes = 4000 if len(sys.argv) == 1 else int(sys.argv[1])

    env = gym.make("MountainCar-v0")

    alphas = [0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0]
    _alpha = alphas[0]

    SARSA_rewards = np.zeros(len(alphas))
    Expected_SARSA_rewards = np.zeros(len(alphas))
    tests = 4

    for test in range(1, tests + 1):
        print(f"Test: {test}")
        for j, _alpha in enumerate(alphas):
            print(f"  Alpha: {_alpha}")
            SARSA_agent = SARSA(
                calculate_states_size(env),
                env.action_space.n,
                alpha=_alpha,
                gamma=0.9,
                epsilon=0.1
            )

            Expected_SARSA_agent = SARSA(
                calculate_states_size(env),
                env.action_space.n,
                alpha=_alpha,
                gamma=0.9,
                epsilon=0.1
            )

            # Train
            SARSA_rewards[j] += run(
                env,
                SARSA_agent,
                "epsilon-greedy",
                episodes,
                "SARSA"
            )
            print(f"SARSA reward: {SARSA_rewards[j]}")
            # env.close()
            Expected_SARSA_rewards[j] += run(
                env,
                Expected_SARSA_agent,
                "epsilon-greedy",
                episodes,
                "Expected_SARSA"
            )
            # env.close()

    for i in range(len(alphas)):
        SARSA_rewards[i] = SARSA_rewards[i] / tests
        Expected_SARSA_rewards[i] = Expected_SARSA_rewards[i] / tests

    plt.plot(alphas, SARSA_rewards, label = 'SARSA')
    plt.plot(alphas, Expected_SARSA_rewards, label = 'Expected SARSA')
    ax1 = plt.subplot()
    ax1.set_xticks(alphas)
    ax1.set_xticklabels(["0.05", "0.1", "0.15", "0.2", "0.3", "0.4", "0.6", "0.8", "1.0"])
    plt.xlabel('x - Alpha')
    plt.ylabel('y - Avg. Reward')
    
    plt.title('SARSA Vs. Expected SARSA')
    plt.legend()
    plt.show()

    env.close()
