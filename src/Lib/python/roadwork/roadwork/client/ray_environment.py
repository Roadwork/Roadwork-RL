import os
import gym
from roadwork.client import ClientDapr
# from roadwork.client import ClientDapr

# https://rllib.readthedocs.io/en/latest/rllib-env.html#configuring-environments
class RayEnvironment(gym.Env):
    # Config specific for Roadwork:
    # rw_sim (e.g. openai)
    # rw_env (e.g. LunarLander-v2)
    # rw_grpc_port
    # rw_grpc_host
    def __init__(self, env_config):
        print(env_config.worker_index, flush=True)
        print(f"==================================================", flush=True)
        print(f"RW_SIM: ", env_config["rw_sim"], " RW_ENV: ", env_config["rw_env"], flush=True)
        print(f"Vector Index: {env_config.vector_index} Worker Index: {env_config.worker_index}", flush=True)
        print(f"==================================================", flush=True)
        self.env = ClientDapr(env_config["rw_sim"])

        self.env.create(env_config["rw_env"], worker_index=env_config.worker_index, vector_index=env_config.vector_index)
        self.action_space = self.env.action_space_info()
        print(f"Action Space: {self.action_space}", flush=True) # Lunar Lander: Nop, Fire Left, Fire Main, Fire Right
        self.observation_space = self.env.observation_space_info()
        print(f"Observation Space: {self.observation_space}", flush=True) 

    def reset(self):
        res = self.env.reset()
        print(res, flush=True)
        return res
    
    def step(self, action):
        res = self.env.step(action)
        return res

    def monitor(self):
        self.env.monitor_start()

    def monitor_stop(self):
        self.env.monitor_stop()