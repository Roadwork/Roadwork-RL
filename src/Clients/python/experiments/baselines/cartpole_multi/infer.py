import gym

from roadwork.client import Client
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

print("===============================================")
print("INFERING")
print("===============================================")
model = PPO2.load("baselines_ppo_cartpole_multi")
env_local = gym.make('CartPole-v1')
obs = env_local.reset()
for i in range(10000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env_local.step(action)
    env_local.render()

env_local.close()