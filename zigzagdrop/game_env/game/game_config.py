import numpy as np

GRID_SIZE = 12
PIECE_SIZE_LIMIT = 3
INTERNAL_GRID_SIZE = GRID_SIZE + PIECE_SIZE_LIMIT
BLOCK_TYPES = 4
PIECE_QUEUE_SIZE = 2
NUM_FEATURES = 7

PIECE_SHAPE_LIST = [
    np.array([
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
    ]),
    np.array([
        [1, 1],
        [1, 0],
    ]),
]

PATTERN_LIST = [
    (
        np.array([
            [1, 1, 1, 1],
        ]),
        [(0, j) for j in range(-INTERNAL_GRID_SIZE, INTERNAL_GRID_SIZE)],
        2,
        300,
    ),
    (
        np.array([
            [1, 1, 1],
            [1, 0, 0],
            [1, 0, 0],
        ]),
        [(0, j) for j in range(-INTERNAL_GRID_SIZE, INTERNAL_GRID_SIZE)] + [(i, 0) for i in range(-INTERNAL_GRID_SIZE, INTERNAL_GRID_SIZE)],
        4,
        500,
    ),
    (
        np.array([
            [0, 1, 1],
            [1, 1, 0],
            [1, 0, 0],
        ]),
        [(k + 1, -k) for k in range(-INTERNAL_GRID_SIZE, INTERNAL_GRID_SIZE)] + [(k + 2, -k) for k in range(-INTERNAL_GRID_SIZE, INTERNAL_GRID_SIZE)],
        4,
        500,
    ),
    (
        np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ]),
        [(i, j) for i in range(-1, 4) for j in range(-1, 4)],
        1,
        500,
    ),
    (
        np.array([
            [1, 0, 0],
            [1, 1, 1],
            [1, 0, 0],
        ]),
        [(1, j) for j in range(-INTERNAL_GRID_SIZE, INTERNAL_GRID_SIZE)] + [(i, 0) for i in range(-INTERNAL_GRID_SIZE, INTERNAL_GRID_SIZE)],
        4,
        500,
    ),
]
