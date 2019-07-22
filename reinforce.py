import argparse
import numpy as np
from itertools import count

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical

import chipgr8
#import chipgr8.games.pong as Pong
from chipgr8.games import Pong1Player as pong
import random

parser = argparse.ArgumentParser(description='PyTorch REINFORCE example')
parser.add_argument('--gamma', type=float, default=0.99, metavar='G',
                    help='discount factor (default: 0.99)')
parser.add_argument('--seed', type=int, default=543, metavar='N',
                    help='random seed (default: 543)')
parser.add_argument('--render', action='store_true',
                    help='render the environment')
parser.add_argument('--log-interval', type=int, default=1, metavar='N',
                    help='interval between training status logs (default: 10)')
args = parser.parse_args()

class Policy(nn.Module):
    def __init__(self):
        super(Policy, self).__init__()
        self.affine1 = nn.Linear(256, 128)
        self.dropout = nn.Dropout(p=0.6)
        self.affine2 = nn.Linear(128, 3)

        self.saved_log_probs = []
        self.rewards = []

    def forward(self, x):
        x = self.affine1(x)
        x = self.dropout(x)
        x = F.relu(x)
        action_scores = self.affine2(x)
        return F.softmax(action_scores, dim=1)


policy = Policy()
optimizer = optim.Adam(policy.parameters(), lr=1e-2)
eps = np.finfo(np.float32).eps.item()

def select_action(state):
    state = torch.from_numpy(state).float().unsqueeze(0)
    probs = policy(state)
    m = Categorical(probs)
    action = m.sample()
    policy.saved_log_probs.append(m.log_prob(action))
    return action.item()


def finish_episode():
    R = 0
    policy_loss = []
    returns = []
    for r in policy.rewards[::-1]:
        R = r + args.gamma * R
        returns.insert(0, R)
    returns = torch.tensor(returns)
    returns = (returns - returns.mean()) / (returns.std() + eps)
    for log_prob, R in zip(policy.saved_log_probs, returns):
        policy_loss.append(-log_prob * R)
    optimizer.zero_grad()
    policy_loss = torch.cat(policy_loss).sum()
    policy_loss.backward()
    optimizer.step()
    del policy.rewards[:]
    del policy.saved_log_probs[:]


def main():
    running_reward = 10
    for i_episode in count(1):

        vm = chipgr8.init(display=True, ROM=pong.ROM, instances=1)
        state = pong.observe(vm)
        ep_reward = 0
        prev_score = 0
        prev_oppon = 0

        #for t in range(1, 10000):
        steps = 0
        while not vm.done():
        #while prev_score <= 8 and prev_oppon <= 8: 
            steps+=1

            # take the action
            # state, reward, done, _ = env.step(action)
            observations = pong.observe(vm)

            state = vm.VM.VRAM

            # select action from policy
            category = select_action(np.array(state))

            reward = 0#observations.score - observations.opponent
            if observations.score > prev_score:
              reward += 1
              prev_score += 1

            if observations.opponent > prev_oppon:
              reward += -1
              prev_oppon += 1

            if observations.score >= 8:
              reward += 1

            #if observations.opponent >= 8:
            #  reward -= 1

            if observations.score >= observations.opponent:
              reward += 1

            #if observations.score < observations.opponent:
            #  reward -= 1

            #if steps > 20000:
            #  reward -= 1

            #if steps > 10000:
            #  reward = 10

            policy.rewards.append(reward)
            ep_reward += reward

            if category == 1: 
              vm.act(0x0010)
            elif category == 2:
              vm.act(0x0002)
            else:
              vm.act(0x0000)

            vm.doneIf(observations.done)

        running_reward = 0.05 * ep_reward + (1 - 0.05) * running_reward
        finish_episode()
        if i_episode % args.log_interval == 0:
            print('Episode {}\tLast reward: {:.2f}\tAverage reward: {:.2f}'.format(
                  i_episode, ep_reward, running_reward))
        #if running_reward > 0:
        #    print("Solved! Running reward is now {} and "
        #          "the last episode runs to {} time steps!".format(running_reward, t))
        #    break


if __name__ == '__main__':
    main()
