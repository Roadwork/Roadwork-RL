import os
import gym
import ray
from ray.rllib.agents import ppo
from roadwork.client import RayEnvironment as RwRayEnvironment

CHECKPOINT_DIR = "/mnt/e/Projects/roadwork-rl/output-server/lunar-lander-checkpoint"
CHECKPOINT_FILE = "checkpoint_100/checkpoint-100"

ray.init()

# Create Agent
config = {
    "rw_sim": "openai",
    "rw_env": "LunarLander-v2",
    "rw_grpc_host": "localhost",
    "rw_grpc_port": 50050
}

test_agent = ppo.PPOTrainer(env=RwRayEnvironment, config={ "env_config": config})
test_agent.restore(f"{CHECKPOINT_DIR}/{CHECKPOINT_FILE}")

# Run Inference
env = RwRayEnvironment(config)
env.monitor()

done = False
state = env.reset()
cumulative_reward = 0

while not done:
    action = test_agent.compute_action(state)
    print(f"Taking action: {action}")
    state, reward, done, _ = env.step(action)
    print(f"Got reward: {reward}")
    cumulative_reward += reward

# env.monitor_stop()
print(cumulative_reward)