import asyncio

import uuid
import gym

from roadwork.client import ClientDapr
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines import PPO2
from stable_baselines.common.vec_env import SubprocVecEnv

if __name__ == '__main__':
    print("===============================================", flush=True)
    print("TRAINING", flush=True)
    print("===============================================", flush=True)
    env = ClientDapr("ActorUnity")
    env.create("Basic-v0")

    for episode in range(2):
      env.reset()

      step = 0
      total_reward = 0
      
      # Note: should go until terminated! @TODO
      for i in range(5):
        action = env.action_space_sample()
        print(f'Action taking: {action}', flush=True)

        obs, reward, done, info = env.step(action)
        print(f'Received:', flush=True)
        print(f'- Obs: {obs}', flush=True)
        print(f'- Rewards: {reward}', flush=True)
        print(f'- Done: {done}', flush=True)
        print(f'- Info: {info}', flush=True)

        total_reward += reward

        if done:
            print("Episode: {0},\tSteps: {1},\tscore: {2}"
                .format(episode, step, total_reward)
            )
            break
