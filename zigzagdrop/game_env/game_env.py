import gymnasium as gym
import numpy as np
import random

from typing import Tuple, Dict, Any

from .action import Action, ActionType, HumanAction
from game_env.game import Game, GRID_SIZE, BLOCK_TYPES, INTERNAL_GRID_SIZE

class GameEnv(gym.Env):
    def __init__(self, action_type: ActionType, screen: Any) -> None:
        self.game = None
        self.action_type = action_type
        self.screen = screen

        self.observation_space = gym.spaces.MultiDiscrete(np.full((BLOCK_TYPES + 1, GRID_SIZE, INTERNAL_GRID_SIZE), 2, dtype=np.int32))

        match self.action_type:
            case ActionType.HUMAN:
                self.action_space = gym.spaces.Discrete(5)
            case ActionType.AI:
                self.action_space = gym.spaces.Discrete(GRID_SIZE * 4)

    def reset(self, seed=None, options=None) -> Tuple[np.array, Dict]:
        self.game = Game(self.screen)
        if seed != None:
            random.seed(seed)
        return self.game.observe(), {}

    def step(self, action: Action) -> Tuple[np.array, float, bool, bool, Dict]:
        reward = 0.0
        
        match self.action_type:
            case ActionType.HUMAN:
                match action.id:
                    case HumanAction.DROP:
                        reward, _ = self.game.place()
                    case HumanAction.MOVE_L:
                        self.game.piece().move(-1)
                    case HumanAction.MOVE_R:
                        self.game.piece().move(+1)
                    case HumanAction.ROT_L:
                        self.game.piece().rot_l()
                    case HumanAction.ROT_R:
                        self.game.piece().rot_r()
            case ActionType.AI:
                pos, rot = action.ai_action_to_tuple()
                self.game.move_and_rot(pos, rot)
                reward, _ = self.game.place()

        return (
            self.game.observe(),
            reward,
            self.game.game_over,
            False,
            {},
        )

    def render(self) -> None:
        self.game.render()