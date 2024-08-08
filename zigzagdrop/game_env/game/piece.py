import numpy as np

from .game_config import *

class Piece:
    def __init__(self, blocks: np.array, pos: int) -> None:
        n, m = blocks.shape
        if not (n == m and 2 <= n <= 3):
            raise ValueError("Piece shape must be either 2x2 or 3x3.")

        self.blocks = blocks
        self.pos = pos

    def rot_l(self) -> None:
        self.blocks = np.rot90(self.blocks)
        self.fix_position()

    def rot_r(self) -> None:
        self.blocks = np.rot90(self.blocks, -1)
        self.fix_position()
        
    def move(self, dx: int) -> None:
        self.pos += dx
        self.fix_position()

    def fix_position(self) -> None:
        n, _ = self.blocks.shape
        ok = False
        while not ok:
            ok = True
            for i in range(n):
                if np.sum(self.blocks[i]) > 0:
                    x = self.pos + i
                    if x < 0:
                        self.pos += 1
                        ok = False
                        break
                    elif x >= GRID_SIZE:
                        self.pos -= 1
                        ok = False
                        break