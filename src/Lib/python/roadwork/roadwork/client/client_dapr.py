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

from dapr.actor import ActorProxy, ActorId
from roadwork.server import RoadworkActorInterface
from asgiref.sync import async_to_sync

#asgiref

class ClientDapr:
    metadata = { 'render.modes': [ 'human' ] }

    def __init__(self, simId):
        # We create a new asyncio event loop per instance
        # This way we can utilize multithreading correctly which would else be prone to collisions on the responses
        # note: collosion = 2 responses at the same time, making an overlap on the first by the second and crashing JSON parsing
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # nest_asyncio.apply() # Patch asyncio
        self.simId = simId

        self.actor_id = "%s-%s-%s" % ("roadwork", self.simId, str(uuid.uuid4().hex)[:8])
        self.proxy = ActorProxy.create(self.simId, ActorId(self.actor_id), RoadworkActorInterface)

    @async_to_sync
    async def _create(self, envId):
      await self.proxy.SimCreate({ 'env_id': envId })
      self.action_space = await self._action_space_info()
      self.observation_space = await self._observation_space_info()
    
    @async_to_sync
    async def _reset(self):
        obs = await self.proxy.SimReset()
        return obs
    
    @async_to_sync
    async def _action_space_sample(self):
        action = await self.proxy.SimActionSample()
        return action

    @async_to_sync
    async def _step(self, action):
        if type(action) == np.int64:
            action = int(action)

        if isinstance(action, np.ndarray):
            action = action.tolist()

        obs, reward, done, info = await self.proxy.SimStep({ 'action': action })
        return [ obs, reward, done, info ]

    @async_to_sync
    async def _monitor_start(self, episode_interval):
        await self.proxy.SimMonitorStart({ 'episode_interval': episode_interval })
    
    @async_to_sync
    async def _monitor_stop(self):
        await self.proxy.SimMonitorStop()

    @async_to_sync
    async def _sim_call_method(self, method, *method_args, **method_kwargs):
        res = await self.proxy.SimCallMethod({ 
            'method': method,
            'args': method_args,
            'kwargs': method_kwargs
        })

        if isinstance(res, list):
            res = res[0] # @todo: assumption is that list gets wrapped again? and then returns one big list, causing us to take element idx 0. But not sure

        return res

    async def _observation_space_info(self):
        observation_space = await self.proxy.SimObservationSpace()
        observation_space = Unserializer.unserializeMeta(observation_space)
        return observation_space

    async def _action_space_info(self):
        action_space = await self.proxy.SimActionSpace()
        action_space = Unserializer.unserializeMeta(action_space)
        return action_space

    @async_to_sync
    async def set_state(self, key, value):
        await self.proxy.SimSetState({ 'key': key, 'value': value })

    @async_to_sync
    async def get_state(self, key):
        res = await self.proxy.SimGetState({ 'key': key })
        return res

    def create(self, envId):
        self._create(envId)

    def observation_space_info(self):
        return self.observation_space
    
    def action_space_info(self):
        return self.action_space
  
    def sim_call_method(self, method, *method_args, **method_kwargs):
        self._sim_call_method(method, method_args, method_kwargs)

    def reset(self):
        obs = self._reset()
        return obs

    def action_space_sample(self):
        action = self._action_space_sample()
        return action

    def step(self, action):
        obs, reward, done, info = self._step(action)
        return [ obs, reward, done, info ]

    def monitor_start(self, episode_interval):
        self._monitor_start(episode_interval)

    def monitor_stop(self):
        self._monitor_stop()