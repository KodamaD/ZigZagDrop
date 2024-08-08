from player import HumanPlayer
from game_env.action import Action, ActionType

import time
import curses
import gymnasium as gym

def play_solo(screen):
    player = HumanPlayer(screen)
    env = gym.make(
        "zigzagdrop-v1",
        action_type = ActionType.HUMAN,
        screen = screen
    )
    env.reset()
    env.render()

    while True:
        env.render()
        action = player.get_action(env.unwrapped.game.direction)
        _, _, done, _, _ = env.step(action)
        time.sleep(0.05)
        if done:
            break

    env.render()
    while True:
        key = screen.getch()
        if key == ord('q'):
            break

def main(screen):
    curses.noecho()
    curses.start_color()
    curses.curs_set(False)
    screen.keypad(True)
    screen.refresh()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_RED)

    time.sleep(1.0)
    play_solo(screen)

if __name__ == "__main__":
    time.sleep(1.0)
    curses.wrapper(main)