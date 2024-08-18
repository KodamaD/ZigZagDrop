import gymnasium as gym
import numpy as np
import random

from typing import Tuple, Dict, Any

from .action import Action, ActionType, HumanAction
from game_env.game import Game, GRID_SIZE, NUM_FEATURES

class GameEnv(gym.Env):
    def __init__(self, action_type: ActionType, screen: Any, slow_render: bool) -> None:
        self.game = None
        self.action_type = action_type
        self.screen = screen
        self.slow_render = slow_render

        self.observation_space = gym.spaces.Box(low=-5.0, high=5.0, shape=(GRID_SIZE * 4, NUM_FEATURES), dtype=np.float32)

        match self.action_type:
            case ActionType.HUMAN:
                self.action_space = gym.spaces.Discrete(5)
            case ActionType.AI:
                self.action_space = gym.spaces.Discrete(GRID_SIZE * 4)

    def reset(self, seed=None, options=None) -> Tuple[np.array, Dict]:
        self.game = Game(self.screen, self.slow_render)
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

    def try_action(self, action: Action) -> bool:
        assert self.action_type == ActionType.AI, "trying action disable for human player"
        pos, rot = action.ai_action_to_tuple()
        new_game = self.game.make_copy()
        new_game.move_and_rot(pos, rot)
        _, _ = new_game.place()
        return new_game.game_over

    def render(self) -> None:
        self.game.render()