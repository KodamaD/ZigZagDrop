import numpy as np
import random
import torch

from typing import List, Any
from collections import deque

class Replay:
    def __init__(self, device: Any, obs: List[np.array], next_obs: List[np.array], action: List[int], reward: List[np.float32], done: List[int]) -> None:
        self.observations = torch.from_numpy(np.array(obs)).to(device)
        self.next_observations = torch.from_numpy(np.array(next_obs)).to(device)
        self.actions = torch.from_numpy(np.array(action)).to(device)
        self.rewards = torch.from_numpy(np.array(reward)).to(device)
        self.dones = torch.from_numpy(np.array(done)).to(device)

class ReplayBuffer:
    def __init__(self, max_capacity: int, device: Any) -> None:
        self.data = deque(maxlen = max_capacity)
        self.device = device
    def add(self, obs: np.array, next_obs: np.array, action: int, reward: np.float32, done: int) -> None:
        self.data.append((obs, next_obs, action, reward, done))
    
    def sample(self, batch_size: int) -> Replay:
        obs = []
        next_obs = []
        action = []
        reward = []
        done = []
        for (p, q, r, s, t) in random.sample(self.data, batch_size):
            obs.append(p)
            next_obs.append(q)
            action.append(r)
            reward.append(s)
            done.append(t)
        return Replay(self.device, obs, next_obs, action, reward, done)

