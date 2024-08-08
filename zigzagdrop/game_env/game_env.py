import gymnasium as gym
import numpy as np
import random

from typing import Any, Tuple

from .action import Action, ActionType, HumanAction
from game_env.game import Game, GRID_SIZE

class GameEnv(gym.Env):
    def __init__(self, action_type, screen) -> None:
        self.game = None
        self.observation = None
        self.action_type = action_type
        self.screen = screen

        self.observation_space = gym.spaces.Discrete(1)

        match self.action_type:
            case ActionType.HUMAN:
                self.action_space = gym.spaces.Discrete(5)
            case ActionType.AI:
                self.action_space = gym.spaces.Tuple((gym.spaces.Discrete(GRID_SIZE), gym.spaces.Discrete(4)))

    def reset(self, seed=None, options=None) -> Tuple[Any, Any]:
        self.game = Game(self.screen, render_mode = (self.action_type == ActionType.HUMAN))
        self.observation = self.game.observe()
        if seed != None:
            random.seed(seed)
        return self.observation, {}

    def step(self, action: Action) -> Tuple[Any, int, bool, bool, Any]:
        reward = 0
        match self.action_type:
            case ActionType.HUMAN:
                match action.id:
                    case HumanAction.DROP:
                        _, reward = self.game.place()
                    case HumanAction.MOVE_L:
                        self.game.piece().move(-1)
                    case HumanAction.MOVE_R:
                        self.game.piece().move(+1)
                    case HumanAction.ROT_L:
                        self.game.piece().rot_l()
                    case HumanAction.ROT_R:
                        self.game.piece().rot_r()
                self.observation = self.game.observe()
            case ActionType.AI:
                pos, rot = action.ai_action_to_tuple()
                self.game.move_and_rot(pos, rot)
                _, reward = self.game.place()
        return (
            self.observation,
            reward,
            self.game.game_over,
            False,
            {},
        )

    def render(self) -> None:
        self.game.render()