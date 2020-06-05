import os
import gym
import ray
from ray.rllib.agents import ppo
from ray.tune.logger import pretty_print

# Import Roadwork Client
from Client import Client

CHECKPOINT_FILE = "/home/xanrin/ray_results/PPO_RoadworkEnv_2020-06-05_17-05-07k5_fimlx/checkpoint_47/checkpoint-47"
SERVER_GRPC_PORT = os.getenv("SERVER_GRPC_PORT", 50050)

print(f"==================================================")
print(f"SERVER_GRPC_PORT: {SERVER_GRPC_PORT}")
print(f"==================================================")

ray.init()

# os.environ["DISPLAY"] = "172.27.208.1:0.0"

class RoadworkEnv(gym.Env):
    def __init__(self, env_config):
        self.env = Client('id-rw-server-openai', 'CartPole-v0')
        self.env.Init("localhost", SERVER_GRPC_PORT)
        self.action_space = self.env.ActionSpaceInfo()
        self.observation_space = self.env.ObservationSpaceInfo()

    def reset(self):
        res = self.env.Reset()
        return res
    
    def step(self, action):
        res = self.env.Step(action)
        return res

    def monitor(self):
        self.env.MonitorStart()

    def monitor_stop(self):
        self.env.MonitorStop()

# Open Agent
test_agent = ppo.PPOTrainer(env=RoadworkEnv, config={ "env_config": {} })
test_agent.restore(CHECKPOINT_FILE)

env = RoadworkEnv({})
env.monitor()

done = False
state = env.reset()
cumulative_reward = 0

while not done:
    print("Running")
    action = test_agent.compute_action(state)
    state, reward, done, _ = env.step(action)
    cumulative_reward += reward

print(cumulative_reward)