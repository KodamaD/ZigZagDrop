from game_env.action import Action, HumanAction

import curses

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
                    return HumanAction.ROT_L
                elif key == curses.KEY_RIGHT:
                    return HumanAction.ROT_R
            case 'Vertical':
                if key == curses.KEY_LEFT:
                    return HumanAction.MOVE_L
                elif key == curses.KEY_RIGHT:
                    return HumanAction.MOVE_R
                elif key == curses.KEY_UP:
                    return HumanAction.ROT_L
                elif key == curses.KEY_DOWN:
                    return HumanAction.ROT_R

        # if keyboard.is_pressed('enter'):
        #     return HumanAction.DROP
        # match direction:
        #     case 'Horizontal':
        #         if keyboard.is_pressed('up'):
        #             return HumanAction.MOVE_L
        #         elif keyboard.is_pressed('down'):
        #             return HumanAction.MOVE_R
        #         elif keyboard.is_pressed('left'):
        #             return HumanAction.ROT_L
        #         elif keyboard.is_pressed('left'):
        #             return HumanAction.ROT_R
        #     case 'Vertical':
        #         if keyboard.is_pressed('left'):
        #             return HumanAction.MOVE_L
        #         elif keyboard.is_pressed('right'):
        #             return HumanAction.MOVE_R
        #         elif keyboard.is_pressed('up'):
        #             return HumanAction.ROT_L
        #         elif keyboard.is_pressed('down'):
        #             return HumanAction.ROT_R