import asyncio

import uuid
import gym

from roadwork.client import ClientDapr

print("===============================================", flush=True)
print("DEMO: SYNC STATE MANAGER", flush=True)
print("===============================================", flush=True)
print("Creating Environment", flush=True)
env = ClientDapr("ActorOpenAI")
env.create("CartPole-v1")

print("Action Space Info", flush=True)
print(env.action_space_info(), flush=True)

print("Observation Space Info", flush=True)
print(env.observation_space_info(), flush=True)

print("Setting State", flush=True)
env.set_state("test", "Some Testing Object")

print("Getting State", flush=True)
res = env.get_state("test")
print(res)