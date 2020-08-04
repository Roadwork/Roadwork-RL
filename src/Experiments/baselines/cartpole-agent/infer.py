    # mean_reward, std_reward = evaluate_policy(model, model.get_env()[0], n_eval_episodes=10)
    # print(f"Mean Reward: {mean_reward}; Std Reward: {std_reward}")
    # evaluate_actor_id = model.get_env()[0].actor_id
    # print(f"Env ID: {evaluate_actor_id}")

import gym

from roadwork.client import ClientDapr
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

def env_create():
    env = ClientDapr("ActorUnity")
    env.create("CartPole-v1")
    
    print(f"[Client] Created Actor {env.actor_id}", flush=True)

    return env

print("===============================================")
print("INFERING")
print("===============================================")
model = PPO2.load("baselines_ppo_cartpole")
env_local = env_create()

# Start monitoring
print("[Client] Starting to monitor", flush=True)
env_local.monitor_start(1)

# Run Experiment
obs = env_local.reset()
is_done = False

while not(is_done):
    action, _states = model.predict(obs)
    obs, rewards, is_done, info = env_local.step(action)

# Stop Monitoring
env_local.monitor_stop()
print("[Client] Stopping Monitor", flush=True)
print("[Client] Done", flush=True)