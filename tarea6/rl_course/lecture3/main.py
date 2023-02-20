import gym
import time
import numpy as np
import gym_environments
from agent3 import MonteCarlo


def train(env, agent, method, episodes):
    
    for i in range(episodes):
        print(i)
        observation, _ = env.reset()
        if method == "deterministic":
            observation = np.random.randint(0,9)

        terminated, truncated = False, False
        while not (terminated or truncated):
            # print("asking for action"))
            if method == "deterministic":
                observation = np.random.randint(0, 9)
            action = agent.get_action(observation)

            # print("got action {} in state {}".format(action, observation))
            new_observation, reward, terminated, truncated, _ = env.step(action)
            agent.update(observation, action, reward, terminated)
            observation = new_observation


def play(env, agent):
    observation, _ = env.reset()
    terminated, truncated = False, False
    while not (terminated or truncated):
        action = agent.get_best_action(observation)
        observation, _, terminated, truncated, _ = env.step(action)
        env.render()
        time.sleep(1)


if __name__ == "__main__":
    env = gym.make("RobotMaze-v0", render_mode="human")
    agent = MonteCarlo(
        env.observation_space.n, env.action_space.n, gamma=0.9, epsilon=0.9
    )

    print("entering train")
    train(env, agent, "deterministic", episodes=50)
    print("exited train")
    agent.render()

    play(env, agent)

    env.close()
