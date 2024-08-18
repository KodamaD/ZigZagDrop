from config import *
from player import *
from game_env.action import ActionType

import time
import curses
import gymnasium as gym
from pathlib import Path

def play_solo(screen):
    player = HumanPlayer(screen)
    env = gym.make(
        "zigzagdrop-v1",
        action_type = ActionType.HUMAN,
        screen = screen,
        slow_render = True,
    )
    env.reset()
    env.render()

    while True:
        env.render()
        action = player.get_action(env.unwrapped.game.direction())
        _, _, done, _, _ = env.step(action)
        time.sleep(0.05)
        if done:
            break

    env.render()
    while True:
        key = screen.getch()
        if key == ord('q'):
            break
    env.close()

def play_ai(screen, model_name, slow_render):
    model_path = Path(__file__).parent.joinpath("learning", "runs", model_name, "train.model")
    player = AIPlayer(model_path)
    env = gym.make(
        "zigzagdrop-v1",
        action_type = ActionType.AI,
        screen = screen,
        slow_render = (slow_render == "S"),
    )
    obs, _ = env.reset()
    env.render()

    while True:
        env.render()
        action = player.get_action(env, obs)
        obs, _, done, _, _ = env.step(action)
        if done:
            break

    env.render()
    while True:
        key = screen.getch()
        if key == ord('q'):
            break
    env.close()

def main(screen, player_type, model_name, slow_render):
    curses.noecho()
    curses.start_color()
    curses.curs_set(False)
    screen.keypad(True)
    screen.refresh()    

    curses.init_pair(Colors.BLACK, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(Colors.WHITE_BG, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(Colors.WHITE_FG, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(Colors.RED_FG, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(Colors.BLOCKS[1], curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(Colors.BLOCKS[2], curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(Colors.BLOCKS[3], curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(Colors.BLOCKS[4], curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(Colors.BLOCKS[5], curses.COLOR_BLACK, curses.COLOR_BLUE)

    time.sleep(0.5)
    
    if player_type == "A":
        play_ai(screen, model_name, slow_render)
    else:
        play_solo(screen)

if __name__ == "__main__":
    time.sleep(0.5)
    player_type = input("Choose player [A or H]: ")
    if player_type == "A":
        model_name = input("Choose model: ")
        slow_render = input("Render mode [S or F]: ")
    else:
        model_name = ""
        slow_render = ""
    curses.wrapper(main, player_type, model_name, slow_render)