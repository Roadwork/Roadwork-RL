import os
import grpc
import sys
import numpy as np
import grpc

import gym.spaces.utils as gym_utils

# Roadwork
from roadwork.json import Unserializer

import uuid
import asyncio

# Needed for patching asyncio to allow .get_event_loop()
import nest_asyncio 

from dapr.actor import ActorProxy, ActorId
from roadwork.server import RoadworkActorInterface

class ClientDapr:
    metadata = { 'render.modes': [ 'human' ] }

    def __init__(self, simId):
        nest_asyncio.apply() # Patch asyncio
        self.simId = simId

        self.actor_id = "%s-%s-%s" % ("roadwork", self.simId, str(uuid.uuid4().hex)[:8])
        self.proxy = ActorProxy.create(self.simId, ActorId(self.actor_id), RoadworkActorInterface)

    def create(self, envId):
        asyncio.get_event_loop().run_until_complete(self.proxy.SimCreate({ 'env_id': envId }))

        print("[Roadwork][Client] Getting Action Space")
        self.action_space = asyncio.get_event_loop().run_until_complete(self._action_space_info())

        print("[Roadwork][Client] Getting Observation Space")
        self.observation_space = asyncio.get_event_loop().run_until_complete(self._observation_space_info())

    async def _observation_space_info(self):
        observation_space = await self.proxy.SimObservationSpace()
        observation_space = Unserializer.unserializeMeta(observation_space)
        return observation_space

    async def _action_space_info(self):
        action_space = await self.proxy.SimActionSpace()
        action_space = Unserializer.unserializeMeta(action_space)
        return action_space

    def observation_space_info(self):
        return self.observation_space
    
    def action_space_info(self):
        return self.action_space

    def reset(self):
        obs = asyncio.get_event_loop().run_until_complete(self.proxy.SimReset())
        return obs

    def action_space_sample(self):
        action = asyncio.get_event_loop().run_until_complete(self.proxy.SimActionSample())
        return action

    def step(self, action):
        if type(action) == np.int64:
            action = int(action)

        obs, reward, done, info = asyncio.get_event_loop().run_until_complete(self.proxy.SimStep({ 'action': action }))
        return [ obs, reward, done, info ]

    def monitor_start(self, episode_interval):
        asyncio.get_event_loop().run_until_complete(self.proxy.SimMonitorStart({ 'episode_interval': episode_interval }))

    def monitor_stop(self):
        asyncio.get_event_loop().run_until_complete(self.proxy.SimMonitorStop())