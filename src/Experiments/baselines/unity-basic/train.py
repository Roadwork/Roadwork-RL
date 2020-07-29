import asyncio

import uuid
import gym

from roadwork.client import ClientDapr
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines import PPO2
from stable_baselines.common.vec_env import SubprocVecEnv

def env_create():
    env = ClientDapr("ActorUnity")
    env.create("Basic-v0")
    print(f"[Client] Created Sim {env.actor_id}", flush=True)

    return env

if __name__ == '__main__':
    print("===============================================", flush=True)
    print("TRAINING", flush=True)
    print("===============================================", flush=True)
    cpu = 1
    env = SubprocVecEnv([ lambda: env_create() for _ in range(cpu) ])

    model = PPO2(MlpPolicy, env, verbose=1, tensorboard_log="./output/tensorboard")
    model.learn(total_timesteps=100000)
    print("[Client][Train] Saving Model", flush=True)
    model.save("baselines_ppo_cartpole")
    print("[Client][Train] DONE", flush=True)

    # Evaluate
    # mean_reward, std_reward = evaluate_policy(model, model.get_env()[0], n_eval_episodes=10)
    # print(f"Mean Reward: {mean_reward}; Std Reward: {std_reward}")
    # evaluate_actor_id = model.get_env()[0].actor_id
    # print(f"Env ID: {evaluate_actor_id}")

