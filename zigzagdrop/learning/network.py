import torch.nn as nn

import sys
sys.path.append('../')
from game_env.game import BLOCK_TYPES, GRID_SIZE, INTERNAL_GRID_SIZE

class QNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            nn.Conv2d(BLOCK_TYPES + 1, 2 * (BLOCK_TYPES + 1), kernel_size=5, padding=2),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.ReLU(),
            nn.Dropout(0.25),
            nn.Conv2d(2 * (BLOCK_TYPES + 1), 4 * (BLOCK_TYPES + 1), kernel_size=3, padding=1),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.ReLU(),
            nn.Dropout(0.25),
            nn.Flatten(),
            nn.Linear(4 * (BLOCK_TYPES + 1) * (GRID_SIZE // 4) * (INTERNAL_GRID_SIZE // 4), 120),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(84, GRID_SIZE * 4),
        )

    def forward(self, x):
        return self.network(x)