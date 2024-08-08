from gymnasium.envs.registration import register

from .action import *
from .game_env import GameEnv

register(
    id="zigzagdrop-v1",
    entry_point="game_env:GameEnv",
)