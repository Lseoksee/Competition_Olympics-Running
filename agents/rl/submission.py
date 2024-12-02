import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical

import numpy as np

from constants import DEVICE

class Actor(nn.Module):
    def __init__(self, state_space, action_space, hidden_size=64, cnn=False):
        super(Actor, self).__init__()
        self.is_cnn = cnn
        self.linear_in = nn.Linear(state_space, hidden_size)
        self.action_head = nn.Linear(hidden_size, action_space)

    def forward(self, x):
        if self.is_cnn:
            x = self.encoder(x)
        x = F.relu(self.linear_in(x))
        action_prob = F.softmax(self.action_head(x), dim=1)
        return action_prob


class Critic(nn.Module):
    def __init__(self, state_space, hidden_size=64, cnn=False):
        super(Critic, self).__init__()
        self.is_cnn = cnn
        self.linear_in = nn.Linear(state_space, hidden_size)
        self.state_value = nn.Linear(hidden_size, 1)

    def forward(self, x):
        if self.is_cnn:
            x = self.encoder(x)
        x = F.relu(self.linear_in(x))
        value = self.state_value(x)
        return value

#INFO: 이건 사용 안됨
actions_map = actions_map = {key: [0, 10 * key] for key in range(36)}

class RLAgent(object):
    def __init__(self, obs_dim, act_dim, num_agent):
        self.obs_dim = obs_dim
        self.act_dim = act_dim
        self.num_agent = num_agent
        self.device = (
            "cuda" if torch.cuda.is_available() and DEVICE == "cuda" else "cpu"
        )
        self.actor = Actor(self.obs_dim, self.act_dim).to(self.device)

    def choose_action(self, obs):
        """
        obs가 환경데이터 인데 해당 환경데이터를 2차원으로 직렬화 한다음에 최대값 뽑아주는거인듯
        """
        state = torch.from_numpy(obs).float().unsqueeze(0).to(self.device)
        with torch.no_grad():
            action_prob = self.actor(state).to(self.device)

        action = torch.argmax(action_prob)
        return action.item()

    def load_model(self, filename):
        self.actor.load_state_dict(torch.load(filename))

#INFO: 이건 사용 안됨
def my_controller(agent: RLAgent, observation_list, action_space_list, is_act_continuous):
    obs_dim = 25 * 25
    obs = observation_list["obs"].copy().flatten()
    actions_raw = agent.choose_action(obs)
    actions = actions_map[actions_raw] # type: ignore
    wrapped_actions = [[actions[0]], [actions[1]]]
    return wrapped_actions
