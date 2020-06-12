import os
import gym
from roadwork.client.client import Client

# https://rllib.readthedocs.io/en/latest/rllib-env.html#configuring-environments
class RayEnvironment(gym.Env):
    # Config specific for Roadwork:
    # rw_sim (e.g. openai)
    # rw_env (e.g. LunarLander-v2)
    # rw_grpc_port
    # rw_grpc_host
    def __init__(self, env_config):
        print(f"==================================================")
        print(f"SERVER_GRPC_PORT: ", env_config["rw_grpc_port"])
        print(f"==================================================")

        self.env = Client(env_config["rw_sim"], env_config["rw_env"])
        self.env.init(env_config["rw_grpc_host"], env_config["rw_grpc_port"])
        self.action_space = self.env.action_space_info()
        print(f"Action Space: {self.action_space}") # Lunar Lander: Nop, Fire Left, Fire Main, Fire Right
        self.observation_space = self.env.observation_space_info()
        print(f"Observation Space: {self.observation_space}") 

    def reset(self):
        res = self.env.reset()
        return res
    
    def step(self, action):
        res = self.env.step(action)
        return res

    def monitor(self):
        self.env.monitor_start()

    def monitor_stop(self):
        self.env.monitor_stop()