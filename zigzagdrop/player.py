from game_env.action import Action, HumanAction
from learning.network import QNetwork

import curses
import torch
import numpy as np

from copy import deepcopy

class HumanPlayer:
    def __init__(self, screen) -> None:
        self.screen = screen

    def get_action(self, direction) -> Action:
        return Action(self._get_action(direction))

    def _get_action(self, direction) -> HumanAction:
        key = self.screen.getch()

        if key == curses.KEY_ENTER or key == ord('\n') or key == ord('\r'):
            return HumanAction.DROP
        match direction:
            case 'Horizontal':
                if key == curses.KEY_UP:
                    return HumanAction.MOVE_R
                elif key == curses.KEY_DOWN:
                    return HumanAction.MOVE_L
                elif key == curses.KEY_LEFT:
                    return HumanAction.ROT_R
                elif key == curses.KEY_RIGHT:
                    return HumanAction.ROT_L
            case 'Vertical':
                if key == curses.KEY_LEFT:
                    return HumanAction.MOVE_L
                elif key == curses.KEY_RIGHT:
                    return HumanAction.MOVE_R
                elif key == curses.KEY_UP:
                    return HumanAction.ROT_L
                elif key == curses.KEY_DOWN:
                    return HumanAction.ROT_R
                
class AIPlayer:
    def __init__(self, model_path: str) -> None:
        self.model = QNetwork()
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

    def get_action(self, env, obs: np.array) -> Action:
        q_values = self.model(torch.from_numpy(np.expand_dims(obs, 0).astype(np.float32))).squeeze()
        
        best = -1
        for i in range(env.action_space.n):
            if not env.unwrapped.try_action(Action(i)):
                if best == -1:
                    best = i
                else:
                    if q_values[best] < q_values[i]:
                        best = i

        if best == -1:
            return Action(env.action_space.sample())        
        return Action(best)
