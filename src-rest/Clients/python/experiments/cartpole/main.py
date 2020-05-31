# import gym
import numpy as np
import math
from collections import deque

import sys
import os
from Client import Client
import time

DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", 3500)
DAPR_GRPC_PORT = os.getenv("DAPR_GRPC_PORT", 50001)

print(f"==================================================")
print(f"DAPR_PORT_GRPC: {DAPR_GRPC_PORT}; DAPR_PORT_HTTP: {DAPR_HTTP_PORT}")
print(f"==================================================")

class QCartPoleSolver():
    def __init__(self, buckets=(1, 1, 6, 12,), n_episodes=1000, n_win_ticks=195, min_alpha=0.1, min_epsilon=0.1, gamma=1.0, ada_divisor=25, max_env_steps=None, quiet=False, monitor=False):
        self.buckets = buckets # down-scaling feature space to discrete range
        self.n_episodes = n_episodes # training episodes 
        self.n_win_ticks = n_win_ticks # average ticks over 100 episodes required for win
        self.min_alpha = min_alpha # learning rate
        self.min_epsilon = min_epsilon # exploration rate
        self.gamma = gamma # discount factor
        self.ada_divisor = ada_divisor # only for development purposes
        self.quiet = quiet

        self.env = Client("localhost", DAPR_HTTP_PORT, "id-rw-server-openai")
        self.env.Init("CartPole-v0")

        if max_env_steps is not None: self.env._max_episode_steps = max_env_steps
        actionSpaceInfo = self.env.ActionSpaceInfo()
        actionSpaceInfoType = actionSpaceInfo["name"]
        actionSPaceInfoN = actionSpaceInfo["n"]

        print(f"Action Space (Name= {actionSpaceInfoType}; N={actionSPaceInfoN})")
        self.Q = np.zeros(self.buckets + (actionSPaceInfoN,))

    def discretize(self, obs):
        observationSpace = self.env.ObservationSpaceInfo()

        upper_bounds = [observationSpace["high"][0], 0.5, observationSpace["high"][2], math.radians(50)]
        lower_bounds = [observationSpace["low"][0], -0.5, observationSpace["low"][2], -math.radians(50)]

        ratios = [(obs[i] + abs(lower_bounds[i])) / (upper_bounds[i] - lower_bounds[i]) for i in range(observationSpace["shape"][0])]
        new_obs = [int(round((self.buckets[i] - 1) * ratios[i])) for i in range(observationSpace["shape"][0])]
        new_obs = [min(self.buckets[i] - 1, max(0, new_obs[i])) for i in range(observationSpace["shape"][0])]
        return tuple(new_obs)
        return 

    def choose_action(self, state, epsilon):
        return self.env.ActionSpaceSample() if (np.random.random() <= epsilon) else np.argmax(self.Q[state])

    def update_q(self, state_old, action, reward, state_new, alpha):
        self.Q[state_old][action] += alpha * (reward + self.gamma * np.max(self.Q[state_new]) - self.Q[state_old][action])

    def get_epsilon(self, t):
        return max(self.min_epsilon, min(1, 1.0 - math.log10((t + 1) / self.ada_divisor)))

    def get_alpha(self, t):
        return max(self.min_alpha, min(1.0, 1.0 - math.log10((t + 1) / self.ada_divisor)))

    def run(self):
        scores = deque(maxlen=100)
        self.env.MonitorStart()

        for e in range(self.n_episodes):
            current_state = self.discretize(self.env.Reset())

            alpha = self.get_alpha(e)
            epsilon = self.get_epsilon(e)
            done = False
            i = 0

            while not done:
                # self.env.Render()
                action = self.choose_action(current_state, epsilon)

                stepResponse = self.env.Step(action)

                obs = stepResponse["obs"]
                reward = stepResponse["reward"]
                done = stepResponse["isDone"]

                # obs, reward, done, _ = self.env.Step(action)

                new_state = self.discretize(obs)
                self.update_q(current_state, action, reward, new_state, alpha)
                current_state = new_state
                i += 1

            scores.append(i)
            mean_score = np.mean(scores)

            if mean_score >= self.n_win_ticks and e >= 100:
                if not self.quiet: print('Ran {} episodes. Solved after {} trials ✔'.format(e, e - 100))
                return e - 100

            if e % 10 == 0 and not self.quiet:
                print('[Episode {}] - Mean survival time over last 100 episodes was {} ticks.'.format(e, mean_score))
            
        if not self.quiet: print('Did not solve after {} episodes 😞'.format(e))
        
        self.env.MonitorStop()

        return e

if __name__ == "__main__":
    solver = QCartPoleSolver()
    solver.run()
    # gym.upload('tmp/cartpole-1', api_key='')