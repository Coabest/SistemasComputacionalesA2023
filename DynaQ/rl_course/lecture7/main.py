import sys
import gym
import gym_environments
import numpy as np
from agent import DYNAQ
from agent2 import DYNAQPLUS
import matplotlib.pyplot as plt


def run(env, agent, selection_method, episodes):
    steps_per_episode = []
    for episode in range(1, episodes+1):
        steps = 0
        print(f"Episode: {episode}")
        observation, _ = env.reset()
        agent.start_episode()
        terminated, truncated = False, False
        while not (terminated or truncated):
            action = agent.get_action(observation, selection_method)
            next_observation, reward, terminated, truncated, _ = env.step(action)
            steps += 1
            agent.update_q(observation, action, next_observation, reward)
            agent.update_model(observation, action, reward, next_observation)
            observation = next_observation
        if selection_method == "epsilon-greedy":
            for _ in range(100):
                state = np.random.choice(list(agent.visited_states.keys()))
                action = np.random.choice(agent.visited_states[state])
                reward, next_state = agent.model[(state, action)]
                agent.update_q(state, action, next_state, reward)
        steps_per_episode.append(steps)
    return steps_per_episode


if __name__ == "__main__":
    environments = ["Princess-v0", "Blocks-v0"]
    id = 1 if len(sys.argv) < 2 else int(sys.argv[1])
    episodes = 7 if len(sys.argv) < 3 else int(sys.argv[2])

    env = gym.make(environments[id])

    steps_DQ = np.zeros(episodes)
    steps_DQPlus = np.zeros(episodes)
    runs = 1

    bestEpisode_DQ = 1e9
    bestEpisode_DQPlus = 1e9
    worstEpisode_DQ = -1
    worstEpisode_DQPlus = -1

    for i in range(runs):
        DQ_agent = DYNAQ(
            env.observation_space.n,
            env.action_space.n,
            alpha=1,
            gamma=0.95,
            epsilon=0.1
        )
        DQ_run = run(env, DQ_agent, "epsilon-greedy", episodes )
        bestEpisode_DQ = np.min(DQ_run)
        worstEpisode_DQ = np.max(DQ_run)
        steps_DQ += DQ_run

        DQPlus_agent = DYNAQPLUS(
            env.observation_space.n,
            env.action_space.n,
            alpha=1,
            gamma=0.95,
            epsilon=0.1,
            kappa=1e-4
        )
        DQPLus_run = run(env, DQPlus_agent, "epsilon-greedy", episodes)
        bestEpisode_DQPlus = np.min(DQPLus_run)
        worstEpisode_DQPlus = np.max(DQPLus_run)
        steps_DQPlus += DQPLus_run
    
    steps_DQ = steps_DQ / runs
    steps_DQPlus = steps_DQPlus / runs

    print(f"Best: {bestEpisode_DQ} Worst: {worstEpisode_DQ}  - DynaQ")
    print(f"Best: {bestEpisode_DQPlus} Worst: {worstEpisode_DQPlus}  - DynaQPlus")

    plt.plot(steps_DQ, label = 'Dyna-Q')
    plt.plot(steps_DQPlus, label = 'Dyna-Q+')
    plt.xlabel('x - Episodes')
    plt.ylabel('y - Steps per episode')
    
    plt.title('Dyna-Q Vs. Dyna-Q+')
    plt.legend()
    plt.show()

    steps_difference = 0
    for i in range(episodes):
        steps_difference += int(steps_DQ[i] - steps_DQPlus[i])

    print(f"\nIn total Dyna-Q+ took {steps_DQPlus} less steps than Dyna-Q")

    plt.plot(steps_DQ - steps_DQPlus, label = 'DynaQPLus - DynaQ')
    plt.xlabel('x - Episodes')
    plt.ylabel('y - Diference in steps per episode')
    
    plt.title('Dyna-Q Vs. Dyna-Q+ Difference')
    plt.legend()
    plt.show()


    env.close()
