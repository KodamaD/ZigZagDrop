import numpy as np

from typing import Tuple, List
from .game_config import *

class Grid:
    def __init__(self, grid: np.array) -> None:
        n, m = grid.shape
        if not (n == INTERNAL_GRID_SIZE and m == INTERNAL_GRID_SIZE):
            raise ValueError(f"Grid size must be {INTERNAL_GRID_SIZE}x{INTERNAL_GRID_SIZE}.")
        
        self.grid = grid
    
    def place_horizontal(self, sy: int, blocks: np.array) -> List[Tuple[int, int]]:
        n, m = blocks.shape
        ret = []
        for dy in range(n):
            y = sy + dy
            if np.sum(blocks[dy]) == 0:
                continue
            if not (0 <= y < GRID_SIZE):
                raise ValueError(f"y={y} out of range [0, {GRID_SIZE}).")
            x = 0
            while self.grid[x][y] != 0:
                x += 1
            for i in range(m):
                if blocks[dy][i] == 0:
                    continue
                if x >= INTERNAL_GRID_SIZE:
                    break
                self.grid[x][y] = blocks[dy][i]
                ret.append((x, y))
                x += 1
        return ret

    def place_vertical(self, sx: int, blocks: np.array) -> List[Tuple[int, int]]:
        n, m = blocks.shape
        ret = []
        for dx in range(n):
            x = sx + dx
            if np.sum(blocks[dx]) == 0:
                continue
            if not (0 <= x < GRID_SIZE):
                raise ValueError(f"x={x} out of range [0, {GRID_SIZE}).")
            y = 0
            while self.grid[x][y] != 0:
                y += 1
            for i in range(m):
                if blocks[dx][i] == 0:
                    continue
                if y >= INTERNAL_GRID_SIZE:
                    break
                self.grid[x][y] = blocks[dx][i]
                ret.append((x, y))
                y += 1
        return ret

    def calc_features(self) -> List[float]:
        zigs = 0
        far = 0
        count = 0
        dist = 0
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] != 0:
                    if i > 0 and self.grid[i - 1][j] == 0:
                        zigs += 1
                    if j > 0 and self.grid[i][j - 1] == 0:
                        zigs += 1
                    far = max(far, i + j)
                    count += 1
                    dist += GRID_SIZE - i - j - 1                    
        l = 0
        t = 0
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x = self.grid[i][j]
                if x == 0:
                    continue
                if x == self.grid[i + 1][j]:
                    if x == self.grid[i + 2][j]:
                        l += 1
                    if x == self.grid[i][j + 1]:
                        t += 1
                    if x == self.grid[i + 1][j + 1]:
                        t += 1
                    if j > 0:
                        if x == self.grid[i][j - 1]:
                            t += 1
                        if x == self.grid[i + 1][j - 1]:
                            t += 1
                if x == self.grid[i][j + 1]:
                    if x == self.grid[i][j + 2]:
                        l += 1
        return [
            zigs / (GRID_SIZE ** 2), 
            far / GRID_SIZE,
            dist / (GRID_SIZE ** 3),
            count / (GRID_SIZE ** 2),
            l / (GRID_SIZE ** 2),
            t / (GRID_SIZE ** 2)
        ]

    def fix_horizontal(self) -> None:
        for y in range(INTERNAL_GRID_SIZE):
            blocks = []
            for x in range(INTERNAL_GRID_SIZE - y - 1):
                if self.grid[x][y] != 0:
                    blocks.append(self.grid[x][y])
                    self.grid[x][y] = 0
            for x, b in enumerate(blocks):
                self.grid[x][y] = b
                        
    def fix_vertical(self) -> None:
        for x in range(INTERNAL_GRID_SIZE):
            blocks = []
            for y in range(INTERNAL_GRID_SIZE - x - 1):
                if self.grid[x][y] != 0:
                    blocks.append(self.grid[x][y])
                    self.grid[x][y] = 0
            for y, b in enumerate(blocks):
                self.grid[x][y] = b

    def is_game_over(self) -> bool:
        for i in range(GRID_SIZE):
            if self.grid[i][GRID_SIZE - i - 1] != 0:
                return True
        return False

    def check_patterns(self) -> Tuple[np.array, int]:
        cleared = np.zeros_like(self.grid, dtype=np.int32)
        score_sum = 0

        for rotation in range(4):
            for (pattern, clear, rotation_limit, score) in PATTERN_LIST:
                if rotation >= rotation_limit:
                    continue
                
                n, m = pattern.shape
                
                def matches(sx, sy):
                    last = 0
                    for dx in range(n):
                        for dy in range(m):
                            x = sx + dx
                            y = sy + dy
                            if pattern[dx][dy] == 1:
                                if not (0 <= x < INTERNAL_GRID_SIZE and 0 <= y < INTERNAL_GRID_SIZE and self.grid[x][y] != 0):
                                    return False
                                if not (last == 0 or last == self.grid[x][y]):
                                    return False
                                last = self.grid[x][y]
                    return True
                                    
                for sx in range(-(n - 1), INTERNAL_GRID_SIZE):
                    for sy in range(-(m - 1), INTERNAL_GRID_SIZE):
                        if matches(sx, sy):
                            for (dx, dy) in clear:
                                x = sx + dx
                                y = sy + dy
                                if 0 <= x < INTERNAL_GRID_SIZE and 0 <= y < INTERNAL_GRID_SIZE:
                                    cleared[x][y] = 1    
                            score_sum += score
                        
            self.grid = np.rot90(self.grid)
            cleared = np.rot90(cleared)
            
        return cleared, score_sum

    def clear_blocks(self, clear: np.array) -> None:
        self.grid = np.multiply(self.grid, 1 - clear)