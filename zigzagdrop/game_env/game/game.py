import random
import numpy as np

import curses
import time

from typing import Any, Tuple, Dict
from copy import deepcopy
from collections import deque

from .grid import Grid
from .piece import Piece
from .game_config import *

import sys
sys.path.append('.../')
from config import *

class Game:
    def __init__(self, screen: Any) -> None:
        self.grid = Grid(np.zeros((INTERNAL_GRID_SIZE, INTERNAL_GRID_SIZE), dtype=np.int32))
        self.pieces = deque()
        self.directions = deque()

        self.turn = 0
        self.points = 0
        self.score = 0.0
        self.game_over = False
        
        self.screen = screen

        self._load_data()

    def _load_data(self) -> None:
        while len(self.pieces) < PIECE_QUEUE_SIZE + 1:
            blocks = deepcopy(random.choice(PIECE_SHAPE_LIST))
            n, m = blocks.shape
            for i in range(n):
                for j in range(m):
                    if blocks[i][j] != 0:
                        blocks[i][j] = random.randint(1, BLOCK_TYPES)
            self.pieces.append(Piece(blocks, GRID_SIZE // 2 - n // 2))
        while len(self.directions) < PIECE_QUEUE_SIZE + 1:
            self.directions.append(random.choice(['Horizontal', 'Vertical']))

    def piece(self) -> Piece:
        return self.pieces[0]
    
    def direction(self) -> str:
        return self.directions[0]

    def move_and_rot(self, pos: int, rot: int) -> None:
        self.piece().move(pos - self.piece().pos)
        for _ in range(rot):
            self.piece().rot_l()

    def place(self) -> Tuple[float, Dict]:
        score_0 = self.score
        
        match self.direction():
            case 'Horizontal':
                self.grid.place_horizontal(self.piece().pos, self.piece().blocks)
            case 'Vertical':
                self.grid.place_vertical(self.piece().pos, self.piece().blocks)
        self.render(0.1)
        self._force_gravity()
        self._recalc_score()
        score_1 = self.score

        self.game_over = self.grid.is_game_over()
        if self.game_over:
            return -100, {}

        self.turn += 1
        self.pieces.popleft()
        self.directions.popleft()
        self._load_data()

        self._force_gravity()
        self._recalc_score()
        self._recalc_score()
        score_2 = self.score

        return (score_1 - score_0) + (score_2 - score_0) * 0.2, {}

    def _recalc_score(self) -> None:
        self.score = 0
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - i - 1):
                if self.grid.grid[i][j] != 0:
                    self.score -= 1.2 ** (i + j)

    def _force_gravity(self) -> None:
        while True:
            match self.direction():
                case 'Horizontal':
                    self.grid.fix_horizontal()
                case 'Vertical':
                    self.grid.fix_vertical()
            self.render(0.1)
            clear, score = self.grid.check_patterns()
            if score == 0:
                break
            self.points += score
            self.grid.clear_blocks(clear)
            self.render(0.1)

    def observe(self) -> np.array:
        ret = np.zeros((BLOCK_TYPES + 1, GRID_SIZE, INTERNAL_GRID_SIZE), dtype=np.int32)
        match self.direction():
            case 'Horizontal':
                for x in range(GRID_SIZE):
                    for y in range(GRID_SIZE):
                        id = self.grid.grid[x][y]
                        if id != 0:
                            ret[id - 1][y][x] = 1
            case 'Vertical':
                for x in range(GRID_SIZE):
                    for y in range(GRID_SIZE):
                        id = self.grid.grid[x][y]
                        if id != 0:
                            ret[id - 1][y][x] = 1
        blocks = self.piece().blocks
        n, m = blocks.shape
        for i in range(n):
            for j in range(m):
                id = blocks[i][j]
                if id != 0:
                    ret[id - 1][self.piece().pos + i][GRID_SIZE + j] = 1
        if self.direction() != self.directions[1]:
            ret[4].fill(1)
        return ret

    def render(self, sleep = 0.0) -> None:
        if self.screen == None:
            return
        
        def write(x: int, y: int, s: str, c: int):
            self.screen.addstr(x, 2 * y, s, curses.color_pair(c))
        
        for i in range(GRID_SIZE + 7):
            write(i, 0, '　' * 150, Colors.BLACK)

        match self.direction():
            case 'Horizontal':
                blocks = self.piece().blocks
                n, m = blocks.shape
                for i in range(n):
                    for j in range(m):
                        write(4 + GRID_SIZE - self.piece().pos - i, GRID_SIZE + 3 + j, '　', Colors.BLOCKS[blocks[i][j]])
                for i in range(GRID_SIZE):
                    write(5 + i, 2 + GRID_SIZE, '・', Colors.WHITE_FG)
            case 'Vertical':
                blocks = self.piece().blocks
                n, m = blocks.shape
                for i in range(n):
                    for j in range(m):
                        write(3 - j, 2 + self.piece().pos + i, '　', Colors.BLOCKS[blocks[i][j]])
                for i in range(GRID_SIZE):
                    write(4, 2 + i, '・', Colors.WHITE_FG)

        for i in range(GRID_SIZE + 1):
            write(5 + i, 1, '　', Colors.WHITE_BG)
            write(5 + GRID_SIZE, 1 + i, '　', Colors.WHITE_BG)
        for i in range(GRID_SIZE + 7):
            write(i, GRID_SIZE + 7, '：', Colors.WHITE_FG)

        for i in range(GRID_SIZE):
            j = GRID_SIZE - i - 1
            write(4 + GRID_SIZE - j, 2 + i, 'ｘ', Colors.RED_FG)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                id = self.grid.grid[i][j]
                if id != 0:
                    write(4 + GRID_SIZE - j, 2 + i, '　', Colors.BLOCKS[id])

        def wide_number(n) -> str:
            wide_list = '０１２３４５６７８９'
            ret = ''
            for c in f'{n}':
                ret += wide_list[ord(c) - ord('0')]
            return ret

        write(1, GRID_SIZE + 9, f'Ｓｃｏｒｅ：{wide_number(self.points)}', Colors.WHITE_FG)
        write(3, GRID_SIZE + 9, f'Ｔｕｒｎ：{wide_number(self.turn)}', Colors.WHITE_FG)
        write(5, GRID_SIZE + 9, 'Ｎｅｘｔ', Colors.WHITE_FG)

        for (k, piece) in enumerate(self.pieces):
            if k == 0:
                continue
            blocks = piece.blocks
            n, m = blocks.shape
            for i in range(n):
                for j in range(m):
                    write(3 + 4 * k + i, GRID_SIZE + 9 + j, '　', Colors.BLOCKS[blocks[i][j]])

        for (k, dir) in enumerate(self.directions):
            if k == 0:
                continue
            write(4 + 4 * k, GRID_SIZE + 15, 'Ｈ' if dir == 'Horizontal' else 'Ｖ', curses.color_pair(7))

        if self.game_over:
            write(15, GRID_SIZE + 9, 'Ｇａｍｅ　Ｏｖｅｒ', Colors.WHITE_FG)
            write(17, GRID_SIZE + 9, 'Ｐｒｅｓｓ　‘ｑ’　ｔｏ　Ｅｘｉｔ', Colors.WHITE_FG)

        self.screen.refresh()
        time.sleep(sleep)