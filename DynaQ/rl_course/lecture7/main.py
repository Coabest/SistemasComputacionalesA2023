import sys
import gym
import gym_environments
import numpy as np
from agent import DYNAQ
from agent2 import DYNAQPLUS
import matplotlib.pyplot as plt


def run(env, agent, selection_method, episodes):
    steps_per_episode = []
    for episode in range(episodes):
        steps = 0
        if episode > 0:
            print(f"Episode: {episode+1}")
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
    episodes = 350 if len(sys.argv) < 3 else int(sys.argv[2])

    env = gym.make(environments[id])

    steps_per_episode_DQ = np.zeros(episodes)
    steps_per_episode_DQPlus = np.zeros(episodes)

    DQ_agent = DYNAQ(
        env.observation_space.n,
        env.action_space.n,
        alpha=1,
        gamma=0.95,
        epsilon=0.1
    )

    DQPlus_agent = DYNAQPLUS(
        env.observation_space.n,
        env.action_space.n,
        alpha=1,
        gamma=0.95,
        epsilon=0.1,
        kappa=1e-4
    )

    # Train
    steps_per_episode_DQ = run(
        env,
        DQ_agent,
        "epsilon-greedy",
        episodes
    )
    # env.close()
    steps_per_episode_DQPlus = run(
        env,
        DQPLus_agent,
        "epsilon-greedy",
        episodes
    )
    # env.close()

    plt.plot(steps_per_episode_DQ, label = 'SARSA')
    plt.plot(steps_per_episode_DQPlus, label = 'Expected SARSA')
    # ax1 = plt.subplot()
    # ax1.set_xticks(alphas)
    # ax1.set_xticklabels(["0.05", "0.1", "0.15", "0.2", "0.3", "0.4", "0.6", "0.8", "1.0"])
    plt.xlabel('x - Episodes')
    plt.ylabel('y - Steps per episode')
    
    plt.title('Dyna-Q Vs. Dyna-Q PLus')
    plt.legend()
    plt.show()

    env.close()

    # Play
    # env = gym.make(environments[id], render_mode="human")
    # run(env, DQ_agent, "greedy", 1)
    # DQ_agent.render()
    # env.close()
