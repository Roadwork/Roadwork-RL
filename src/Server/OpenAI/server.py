# -*- coding: utf-8 -*-
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import datetime

from dapr.actor import Actor, Remindable
# import roadwork.json.serializer as Serializer
from roadwork.json import Serializer
from roadwork.server import RoadworkActorInterface
from roadwork.json import Serializer

# from roadwork.server import Server
import gym
import sys
import os
import traceback
import numpy as np
import logging
import asyncio

logger = logging.getLogger('RW-Server')

class ActorOpenAI(Actor, RoadworkActorInterface):
    def __init__(self, ctx, actor_id):
        super(ActorOpenAI, self).__init__(ctx, actor_id)
        self.env = None # Placeholder
        self.actor_id = actor_id

    async def sim_call_method(self, data) -> object:
        method = data['method']
        args = data['args'] # Array of arguments - [] 
        kwargs = data['kwargs'] # Dict 

        return getattr(self.env, method)(*args, **kwargs)

    async def sim_get_state(self, data) -> object:
        key = data['key']
        has_value, val = await self._state_manager.try_get_state(key)
        return val

    async def sim_set_state(self, data) -> None:
        key = data['key']
        value = data['value']

        print(f'Setting Sim State for key {key}', flush=True)
        await self._state_manager.set_state(key, value)
        await self._state_manager.save_state()

    async def _on_activate(self) -> None:
        """An callback which will be called whenever actor is activated."""
        print(f'Activate {self.__class__.__name__} actor!', flush=True)

    async def _on_deactivate(self) -> None:
        """An callback which will be called whenever actor is deactivated."""
        print(f'Deactivate {self.__class__.__name__} actor!', flush=True)

    async def sim_action_space(self) -> object:
        res = Serializer.serializeMeta(self.env.action_space)
        return res
        
    async def sim_observation_space(self) -> object:
        print(self.env.observation_space, flush=True)
        print(self.env.observation_space.high, flush=True)
        print(self.env.observation_space.low, flush=True)
        res = Serializer.serializeMeta(self.env.observation_space)
        return res

    async def sim_create(self, data) -> None:
        """An actor method to create a sim environment."""
        print(data, flush=True)
        env_id = data['env_id']

        # vector_idx = data['vector_index']
        # worker_idx = data['worker_index']
        # sleep = (vector_idx + 1) * worker_idx * 5
        # print(f"Sleeping for blocking call in assistive-gym env {sleep}", flush=True)
        # await asyncio.sleep(sleep)

        print(f'Creating sim with value {env_id}', flush=True)
        try:
            self.env = gym.make(env_id)
            # if seed:
            #     self.env.seed(seed)
        except gym.error.Error as e:
            print(e, flush=True)
            raise Exception("Attempted to look up malformed environment ID '{}'".format(env_id))
        except Exception as e:
            print(e, flush=True)
            logger.exception('')
            raise Exception(e)
        except:
            print(sys.exc_info())
            traceback.print_tb(sys.exc_info()[2])
            raise

    async def sim_reset(self) -> object:
        observation = self.env.reset()

        # observation is a ndarray, we need to serialize this
        # therefore, change it to list type which is serializable
        if isinstance(observation, np.ndarray):
            observation = observation.tolist()

        return observation

    async def sim_render(self) -> None:
        self.env.render()

    async def sim_monitor_start(self, data) -> None:
        episodeInterval = 10 # Create a recording every X episodes

        if data['episode_interval']:
            episodeInterval = int(data['episode_interval'])

        v_c = lambda count: count % episodeInterval == 0 # Create every X episodes
        self.env = gym.wrappers.Monitor(self.env, f'./output/{self.actor_id}', resume=False, force=True, video_callable=v_c)

    async def sim_monitor_stop(self) -> None:
        self.env.close()

    async def sim_action_sample(self) -> object:
        action = self.env.action_space.sample()
        return action

    async def sim_step(self, data) -> object:
        observation, reward, isDone, info = self.env.step(data['action'])

        # observation is a ndarray, we need to serialize this
        # therefore, change it to list type which is serializable
        if isinstance(observation, np.ndarray):
            observation = observation.tolist()

        return observation, reward, isDone, info