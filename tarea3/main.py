import os

import gym
import gym_environments
import time
# from agent import ValueIteration
from agent import PolicyIteration

# Allowing environment to have sounds
if "SDL_AUDIODRIVER" in os.environ:
    del os.environ["SDL_AUDIODRIVER"]

env = gym.make('FrozenLake-v2', render_mode="human")

# agent = ValueIteration(env.observation_space.n, env.action_space.n, env.P, 0.9)
agent = PolicyIteration(env.observation_space.n, env.action_space.n, env.P, 0.9)
agent.solve(10000)
agent.render()

total_reward = 0
test_sample_size = 10000

for i in range(test_sample_size):
    observation, info = env.reset()
    terminated, truncated = False, False

    # env.render()
    # time.sleep(2)

    while not (terminated or truncated):
        action = agent.get_action(observation)
        observation, reward, terminated, truncated, _ = env.step(action)

    total_reward += reward

print ("Average reward: {}".format(total_reward/test_sample_size))

env.close()
