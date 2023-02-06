from gym.envs.registration import register

register(
    id='TwoArmedBandit-v0',
    entry_point='gym_environments.envs:TwoArmedBanditEnvV0',
)

register(
    id='TwoArmedBandit-v1',
    entry_point='gym_environments.envs:TwoArmedBanditEnvV1',
)

register(
    id='RobotBattery-v0',
    entry_point='gym_environments.envs:RobotBatteryEnvV0',
)

register(
    id='FrozenLake-v2',
    entry_point='gym_environments.envs:FrozenLakeV2',
)

register(
    id='RobotMaze-v0',
    entry_point='gym_environments.envs:RobotMazeEnvV0',
)
