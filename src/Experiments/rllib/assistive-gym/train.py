import os
import gym
import ray
from ray.rllib.agents import ppo
from ray.tune.registry import register_env
# from ray.rllib.env import EnvContext
from roadwork.client import RayEnvironment as RwRayEnvironment

CHECKPOINT_DIR = "/home/xanrin/roadwork-rl-output"
CHECKPOINT_FILE = "last_checkpoint.out"

# register_env("rw_env", lambda config: RwRayEnvironment(config))

def env_creator(env_config):
  return RwRayEnvironment(env_config)

register_env("rw_env", env_creator)

ray.init()
trainer = ppo.PPOTrainer(env="rw_env", config={ 
  "num_workers": 5, 
  # "num_envs_per_worker": 2,
  # "monitor": True,
  "env_config": {
    "rw_sim": "ActorOpenAI",
    "rw_env": "FeedingJaco-v0"
  }
})

print(f"Starting training, you can view process through `tensorboard --logdir={CHECKPOINT_DIR}` and opening http://localhost:6006", flush=True)

# Attempt to restore from checkpoint if possible.
if os.path.exists(f"{CHECKPOINT_DIR}/{CHECKPOINT_FILE}"):
    checkpoint_path = open(f"{CHECKPOINT_DIR}/{CHECKPOINT_FILE}").read()
    print("Restoring from checkpoint path", checkpoint_path, flush=True)
    trainer.restore(checkpoint_path)

try:
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
finally:
  ray.shutdown()