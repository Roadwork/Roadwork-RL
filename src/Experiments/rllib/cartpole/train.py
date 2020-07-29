import os
import gym
import ray
from ray.rllib.agents import ppo
from roadwork.client import RayEnvironment as RwRayEnvironment

CHECKPOINT_DIR = "/mnt/e/Projects/roadwork-rl/output-server/cartpole-checkpoint"
CHECKPOINT_FILE = "last_checkpoint.out"

ray.init()
trainer = ppo.PPOTrainer(env=RwRayEnvironment, config={ "env_config": {
    "rw_sim": "ActorOpenAI",
    "rw_env": "CartPole-v0"
}})

print(f"Starting training, you can view process through `tensorboard --logdir={CHECKPOINT_DIR}` and opening http://localhost:6006", flush=True)

# Attempt to restore from checkpoint if possible.
if os.path.exists(f"{CHECKPOINT_DIR}/{CHECKPOINT_FILE}"):
    checkpoint_path = open(f"{CHECKPOINT_DIR}/{CHECKPOINT_FILE}").read()
    print("Restoring from checkpoint path", checkpoint_path, flush=True)
    trainer.restore(checkpoint_path)

while True:
    results = trainer.train()
    
    rw_date = results["date"]
    rw_timesteps_total = results["timesteps_total"]
    rw_time_total_s = results["time_total_s"]
    rw_episode_reward_mean = results["episode_reward_mean"]
    
    print(f"{rw_date} INFO Step: {rw_timesteps_total}. Time Elapsed: {rw_time_total_s}s Mean Reward: {rw_episode_reward_mean}", flush=True)

    checkpoint_path = trainer.save(CHECKPOINT_DIR)
    print("--> Last checkpoint", checkpoint_path, flush=True)
    with open(f"{CHECKPOINT_DIR}/{CHECKPOINT_FILE}", "w") as f:
        f.write(checkpoint_path)