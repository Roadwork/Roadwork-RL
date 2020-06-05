import os
import gym
import ray
from ray.rllib.agents import ppo

import roadwork as rw

SERVER_GRPC_PORT = os.getenv("SERVER_GRPC_PORT", 50050)
CHECKPOINT_DIR = "/mnt/e/Projects/roadwork-rl/output-server/bipedal-walker-checkpoint"
CHECKPOINT_FILE = "last_checkpoint.out"

ray.init()
trainer = ppo.PPOTrainer(env=rw.RayEnvironment, config={ "env_config": {
    "rw_sim": "openai",
    "rw_env": "BipedalWalkerHardcore-v3",
    "rw_grpc_host": "localhost",
    "rw_grpc_port": 50050
}})

print(f"Starting training, you can view process through `tensorboard --logdir={CHECKPOINT_DIR}` and opening http://localhost:6006")

# Attempt to restore from checkpoint if possible.
if os.path.exists(f"{CHECKPOINT_DIR}/{CHECKPOINT_FILE}"):
    checkpoint_path = open(f"{CHECKPOINT_DIR}/{CHECKPOINT_FILE}").read()
    print("Restoring from checkpoint path", checkpoint_path)
    trainer.restore(checkpoint_path)

while True:
    results = trainer.train()
    
    rw_date = results["date"]
    rw_timesteps_total = results["timesteps_total"]
    rw_time_total_s = results["time_total_s"]
    rw_episode_reward_mean = results["episode_reward_mean"]
    
    print(f"{rw_date} INFO Step: {rw_timesteps_total}. Time Elapsed: {rw_time_total_s}s Mean Reward: {rw_episode_reward_mean}")

    checkpoint_path = trainer.save(CHECKPOINT_DIR)
    print("--> Last checkpoint", checkpoint_path)
    with open(f"{CHECKPOINT_DIR}/{CHECKPOINT_FILE}", "w") as f:
        f.write(checkpoint_path)