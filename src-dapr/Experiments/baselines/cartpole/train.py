import asyncio

import uuid
import gym

from roadwork.client import ClientDapr
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines import PPO2

print("===============================================", flush=True)
print("TRAINING", flush=True)
print("===============================================", flush=True)
env = ClientDapr("ActorOpenAI")
env.create("CartPole-v1")

print("Action Space Info", flush=True)
print(env.action_space_info(), flush=True)

print("Observation Space Info", flush=True)
print(env.observation_space_info(), flush=True)

env.monitor_start(50)

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=5000)
model.save("baselines_ppo_cartpole")

env.monitor_stop()

# Evaluate
mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
print(f"Mean Reward: {mean_reward}; Std Reward: {std_reward}")
print(f"Env ID: {env.actor_id}")

