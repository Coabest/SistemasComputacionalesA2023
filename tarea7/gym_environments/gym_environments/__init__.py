import os
from gym.envs.registration import register

# Allowing environment to have sounds
if "SDL_AUDIODRIVER" in os.environ:
    del os.environ["SDL_AUDIODRIVER"]

register(
    id="TwoArmedBandit-v0",
    entry_point="gym_environments.envs:TwoArmedBanditEnvV0",
)

register(
    id="TwoArmedBandit-v1",
    entry_point="gym_environments.envs:TwoArmedBanditEnvV1",
)

register(
    id="RobotBattery-v0",
    entry_point="gym_environments.envs:RobotBatteryEnvV0",
)

register(
    id="FrozenLake-v2",
    entry_point="gym_environments.envs:FrozenLakeV2",
)

register(
    id="RobotMaze-v0",
    entry_point="gym_environments.envs:RobotMazeEnvV0",
)

register(
    id="Princess-v0",
    entry_point="gym_environments.envs:PrincessEnvV0",
)

register(
    id="Blocks-v0",
    entry_point="gym_environments.envs:BlocksEnvV0",
)
