import os
import gym
import ray
from ray.rllib.agents import ppo
from ray.tune.logger import pretty_print

# Import Roadwork Client
from Client import Client

SERVER_GRPC_PORT = os.getenv("SERVER_GRPC_PORT", 50050)
CHECKPOINT_FILE = "last_checkpoint.out"

print(f"==================================================")
print(f"SERVER_GRPC_PORT: {SERVER_GRPC_PORT}")
print(f"==================================================")

class RoadworkEnv(gym.Env):
    def __init__(self, env_config):
        self.env = Client('id-rw-server-openai', 'CartPole-v0')
        self.env.Init("localhost", SERVER_GRPC_PORT)
        self.action_space = self.env.ActionSpaceInfo()
        self.observation_space = self.env.ObservationSpaceInfo()

        # Start monitoring
        # self.env.MonitorStart()

    def reset(self):
        res = self.env.Reset()
        return res
    
    def step(self, action):
        res = self.env.Step(action)
        return res

ray.init()
trainer = ppo.PPOTrainer(env=RoadworkEnv, config={ "env_config": {} })

# Attempt to restore from checkpoint if possible.
if os.path.exists(CHECKPOINT_FILE):
    checkpoint_path = open(CHECKPOINT_FILE).read()
    print("Restoring from checkpoint path", checkpoint_path)
    trainer.restore(checkpoint_path)

while True:
    results = trainer.train()
    
    rw_date = results["date"]
    rw_timesteps_total = results["timesteps_total"]
    rw_time_total_s = results["time_total_s"]
    rw_episode_reward_mean = results["episode_reward_mean"]
    
    print(f"{rw_date} INFO Step: {rw_timesteps_total}. Time Elapsed: {rw_time_total_s}s Mean Reward: {rw_episode_reward_mean}")

    checkpoint_path = trainer.save()
    print("--> Last checkpoint", checkpoint_path)
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(checkpoint_path)