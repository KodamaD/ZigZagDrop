import random
import numpy as np

from copy import deepcopy
from collections import deque

from .grid import Grid
from .piece import Piece, PIECE_SHAPE_LIST

GRID_SIZE = 12
BLOCK_TYPES = 4
PIECE_QUEUE_SIZE = 2

class Game:
    def __init__(self) -> None:
        self.grid = Grid(np.zeros((GRID_SIZE, GRID_SIZE))),
        self.pieces = deque()
        self.direction = 'Vertical'
        self.score = 0
        self.game_over = False
        self._load_pieces()
        pass

    def _load_pieces(self) -> None:
        while len(self.pieces) < PIECE_QUEUE_SIZE + 1:
            blocks = deepcopy(random.choice(PIECE_SHAPE_LIST))
            n, m = blocks.shape
            for i in range(n):
                for j in range(m):
                    if blocks[i][j] != 0:
                        blocks[i][j] = random.randint(1, BLOCK_TYPES)
            self.pieces.append(Piece(blocks, GRID_SIZE // 2))

    def piece(self) -> Piece:
        return self.pieces[0]

    def operation(self, dx: int, rot: int) -> bool:
        pass

    def opserve(self) -> np.array:
        pass

    def render(self) -> str:
        pass
