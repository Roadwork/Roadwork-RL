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

class ActorOpenAI(Actor, RoadworkActorInterface):
    def __init__(self, ctx, actor_id):
        super(ActorOpenAI, self).__init__(ctx, actor_id)
        self.env = None # Placeholder
        self.actor_id = actor_id

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
        res = Serializer.serializeMeta(self.env.observation_space)
        return res

    async def sim_create(self, data) -> None:
        """An actor method to create a sim environment."""
        env_id = data['env_id']
        # seed = data['seed']

        print(f'Creating sim with value {env_id}', flush=True)
        try:
            self.env = gym.make(env_id)

            # if seed:
            #     self.env.seed(seed)
        except gym.error.Error as e:
            print(e)
            raise Exception("Attempted to look up malformed environment ID '{}'".format(env_id))
        except Exception as e:
            print(e)
            raise Exception(e)
        except:
            print(sys.exc_info())
            traceback.print_tb(sys.exc_info()[2])
            raise

    async def sim_reset(self) -> object:
        observation = self.env.reset()

        # observation is a ndarray, we need to serialize this
        # therefore, change it to list type which is serializable
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
        observation = observation.tolist()

        return observation, reward, isDone, info

    async def get_my_data(self) -> object:
        """An actor method which gets mydata state value."""
        has_value, val = await self._state_manager.try_get_state('mydata')
        print(f'has_value: {has_value}', flush=True)
        return val

    async def set_my_data(self, data) -> None:
        """An actor method which set mydata state value."""
        print(f'set_my_data: {data}', flush=True)
        data['ts'] = datetime.datetime.now(datetime.timezone.utc)
        await self._state_manager.set_state('mydata', data)
        await self._state_manager.save_state()