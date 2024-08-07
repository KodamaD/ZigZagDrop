import numpy as np

from .game import GRID_SIZE, PATTERN_LIST

class Grid:
    def __init__(self, grid: np.array) -> None:
        n, m = grid.shape
        if not (n == GRID_SIZE and m == GRID_SIZE):
            raise ValueError(f"Grid size must be {GRID_SIZE}x{GRID_SIZE}.")
        
        self.grid = grid
    
    def place_horizontal(self, y: int, blocks: np.array) -> bool:
        if not (0 <= y < GRID_SIZE):
            raise ValueError(f"y={y} out of range [0, {GRID_SIZE}).")
        x = 0
        while self.grid[x][y] != 0:
            x += 1
        n = blocks.shape
        for i in range(n):
            if blocks[i] == 0:
                continue
            if x + y >= GRID_SIZE - 1:
                return False
            self.grid[x][y] = blocks[i]
        return True

    def place_vertical(self, x: int, blocks: np.array) -> bool:
        if not (0 <= y < GRID_SIZE):
            raise ValueError(f"x={x} out of range [0, {GRID_SIZE}).")
        y = 0
        while self.grid[x][y] != 0:
            y += 1
        n = blocks.shape
        for i in range(n):
            if blocks[i] == 0:
                continue
            if x + y >= GRID_SIZE - 1:
                return False
            self.grid[x][y] = blocks[i]
        return True

    def fix_horizontal(self) -> None:
        for y in range(GRID_SIZE):
            blocks = []
            for x in range(GRID_SIZE - y - 1):
                if self.grid[x][y] != 0:
                    blocks.append(self.grid[x][y])
                    self.grid[x][y] = 0
            for x, b in enumerate(blocks):
                self.grid[x][y] = b
                        
    def fix_vertical(self) -> None:
        for x in range(GRID_SIZE):
            blocks = []
            for y in range(GRID_SIZE - x - 1):
                if self.grid[x][y] != 0:
                    blocks.append(self.grid[x][y])
                    self.grid[x][y] = 0
            for y, b in enumerate(blocks):
                self.grid[x][y] = b

    def check_patterns(self) -> np.array:
        deleted = np.zeros_like(self.grid)
        
        for rotation in range(4):
            for (pattern, delete, rotation_limit) in PATTERN_LIST:
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
                                if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
                                    return False
                                if not (last == 0 or last == self.grid[x][y]):
                                    return False
                                last = self.grid[x][y]
                    return True
                                    
                for sx in range(-(n - 1), GRID_SIZE):
                    for sy in range(-(m - 1), GRID_SIZE):
                        if matches(sx, sy):
                            for (dx, dy) in delete:
                                x = sx + dx
                                y = sy + dy
                                if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                                    deleted[x][y] = 1    
                        
            self.grid = np.rot90(self.grid)
            deleted = np.rot90(deleted)
            
        return deleted