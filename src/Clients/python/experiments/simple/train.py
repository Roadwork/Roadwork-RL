import gym

from roadwork.client import Client

print("===============================================")
print("TRAINING")
print("===============================================")
env = Client("openai", "CartPole-v1")
env.init("localhost", 50050)

print("Action Space Info")
print(env.action_space_info())

print("Observation Space Info")
print(env.observation_space_info())

env.reset()

action = env.action_space_sample()
print(f"Taking Action: {action}")

env.step(action)


# for i in range(10000):
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env_local.step(action)
#     env_local.render()

# env_local.close()

# model = PPO2(MlpPolicy, env, verbose=1)
# model.learn(total_timesteps=100000)
# model.save("baselines_ppo_cartpole")

# # Evaluate
# mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
# print(f"Mean Reward: {mean_reward}; Std Reward: {std_reward}")