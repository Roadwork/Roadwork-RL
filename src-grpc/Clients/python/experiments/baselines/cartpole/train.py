import gym

from roadwork.client import Client
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines import PPO2

print("===============================================")
print("TRAINING")
print("===============================================")
env = Client("openai", "CartPole-v1")
env.init("localhost", 50050)

print("Action Space Info")
print(env.action_space_info())

print("Observation Space Info")
print(env.observation_space_info())

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=100000)
model.save("baselines_ppo_cartpole")

# Evaluate
mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
print(f"Mean Reward: {mean_reward}; Std Reward: {std_reward}")