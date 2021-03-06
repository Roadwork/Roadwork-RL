import gym

from stable_baselines.common.vec_env import VecEnv

# class RoadworkVecEnv(VecEnv):

from roadwork.client import Client
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

def make_env(env_id, rank):
    def _init():
        env = Client("openai", env_id)
        env.init("localhost", 50050)
        return env
        
    return _init # We need a callable

if __name__ == '__main__':
    print("===============================================")
    print("TRAINING")
    print("===============================================")

    env_id = "CartPole-v1"
    num_envs = 4
    env = DummyVecEnv([make_env(env_id, i) for i in range(num_envs)])

    model = PPO2(MlpPolicy, env, verbose=1)
    model.learn(total_timesteps=100000)
    model.save("baselines_ppo_cartpole_multi")

    # Evaluate
    mean_reward, std_reward = evaluate_policy(model, model.get_env()[0], n_eval_episodes=10)
    print(f"Mean Reward: {mean_reward}; Std Reward: {std_reward}")