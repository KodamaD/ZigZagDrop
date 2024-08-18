

import os
import random
import time
from dataclasses import dataclass

import gymnasium as gym
import numpy as np
import torch
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter

from network import QNetwork
from replay_buffer import ReplayBuffer
from tqdm import tqdm

import sys
sys.path.append('../')
from game_env.action import Action, ActionType
from game_env.game.game_config import GRID_SIZE, NUM_FEATURES

import wandb

@dataclass
class Args:
    # envirionment
    exp_name: str = os.path.basename(__file__)[: -len(".py")]
    seed: int = 202408
    num_envs: int = 1
    torch_deterministic: bool = True
    cuda: bool = True
    wandb_project_name: str = "ZigZagDrop-DQN"
    wandb_entity: str = None
    save_model: bool = False

    # algorithm
    env_id: str = "zigzagdrop-v1"
    total_timesteps: int = 10000
    learning_rate: float = 2.5e-4
    buffer_size: int = 10000
    gamma: float = 0.9
    tau: float = 0.95
    target_network_frequency: int = 200
    batch_size: int = 64
    start_e: float = 1
    end_e: float = 0.05
    exploration_fraction: float = 0.5
    learning_starts: int = 500
    train_frequency: int = 10

def linear_schedule(start_e: float, end_e: float, duration: int, t: int):
    slope = (end_e - start_e) / duration
    return max(slope * t + start_e, end_e)

def train(args: Args):
    run_name = f"{args.env_id}__{args.exp_name}__{args.seed}__{int(time.time())}"

    wandb.init(project="zigzagdrop")

    writer = SummaryWriter(f"runs/{run_name}")
    writer.add_text(
        "hyperparameters",
        "|param|value|\n|-|-|\n%s" % ("\n".join([f"|{key}|{value}|" for key, value in vars(args).items()])),
    )

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.backends.cudnn.deterministic = args.torch_deterministic

    device = torch.device("cuda" if torch.cuda.is_available() and args.cuda else "cpu")
    env = gym.make(args.env_id, action_type = ActionType.AI, screen = None, slow_render = False)
    q_network = QNetwork().to(device)
    optimizer = optim.Adam(q_network.parameters(), lr=args.learning_rate)
    target_network = QNetwork().to(device)
    target_network.load_state_dict(q_network.state_dict())
    rb = ReplayBuffer(args.buffer_size, device)

    start_time = time.time()
    obs, _ = env.reset(seed=args.seed)
    for global_step in tqdm(range(args.total_timesteps)):
        epsilon = linear_schedule(args.start_e, args.end_e, args.exploration_fraction * args.total_timesteps, global_step)
        q_values = q_network(torch.from_numpy(obs).to(device))
        if random.random() < epsilon:
            action = env.action_space.sample()
        else:
            action = torch.argmax(q_values).cpu().item()
    
        next_obs, reward, termination, _, _ = env.step(Action(action))
        rb.add(obs, next_obs, action, reward, int(termination))

        if termination:
            obs, _ = env.reset(seed=args.seed + global_step)
        else:
            obs = next_obs

        if global_step > args.learning_starts:
            if global_step % args.train_frequency == 0:
                data = rb.sample(args.batch_size)
                with torch.no_grad():
                    target_max, _ = torch.reshape(target_network(data.next_observations.flatten(end_dim=1)), (-1,GRID_SIZE*4)).max(dim=1)
                    td_target = data.rewards.flatten() + args.gamma * target_max * (1. - data.dones.flatten())
                    td_target = td_target.float()
                old_val = torch.reshape(q_network(data.observations.flatten(end_dim=1)), (-1,GRID_SIZE*4)).gather(1, data.actions.unsqueeze(0)).squeeze()
                loss = F.huber_loss(td_target, old_val)

                wandb.log({"loss": loss, "q_value": old_val, "target": td_target})

                if global_step % 100 == 0:
                    writer.add_scalar("losses/td_loss", loss, global_step)
                    writer.add_scalar("losses/q_values", old_val.mean().item(), global_step)
                    writer.add_scalar("charts/SPS", int(global_step / (time.time() - start_time)), global_step)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            if global_step % args.target_network_frequency == 0:
                for target_network_param, q_network_param in zip(target_network.parameters(), q_network.parameters()):
                    target_network_param.data.copy_(args.tau * q_network_param.data + (1.0 - args.tau) * target_network_param.data)

    if args.save_model:
        model_path = f"runs/{run_name}/{args.exp_name}.model"
        torch.save(q_network.state_dict(), model_path)
        print(f"model saved to {model_path}")

    wandb.finish()
    env.close()
    writer.close()

if __name__ == "__main__":
    args = Args(save_model=True)
    train(args)