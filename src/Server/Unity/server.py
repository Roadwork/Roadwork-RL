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
import gym.spaces as spaces
import sys
import os
import traceback
import numpy as np

from gym_unity.envs import UnityToGymWrapper
from mlagents_envs.environment import UnityEnvironment

# https://github.com/Unity-Technologies/ml-agents/blob/release_4_docs/docs/Python-API.md#interacting-with-a-unity-environment
class ActorUnity(Actor, RoadworkActorInterface):
    def __init__(self, ctx, actor_id):
        super(ActorUnity, self).__init__(ctx, actor_id)
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

    # see behavior_spec: https://github.com/Unity-Technologies/ml-agents/blob/release_4_docs/docs/Python-API.md#interacting-with-a-unity-environment
    # behavior_spec.action_type and behavior_spec.action_shape is what we need here
    async def sim_action_space(self) -> object:
        behavior_names = list(self.env.behavior_specs.keys()) # the behavior_names which map to a Behavior Spec with observation_shapes, action_type, action_shape
        behavior_idx = 0 # we currently support only 1 behavior spec! even though Unity can support multiple (@TODO)
        behavior_spec = self.env.behavior_specs[behavior_names[behavior_idx]]

        print(f"Action Type: {behavior_spec.action_type}", flush=True)
        print(f"Action Shape: {behavior_spec.action_shape}", flush=True)

        # We can use /src/Lib/python/roadwork/roadwork/json/unserializer.py as an example
        # Currently only ActionType.DISCRETE implemented, all ActionTypes can be found here: https://github.com/Unity-Technologies/ml-agents/blob/3901bad5b0b4e094e119af2f9d0d1304ad3f97ae/ml-agents-envs/mlagents_envs/base_env.py#L247
        # Note: Unity supports DISCRETE or CONTINUOUS action spaces @TODO: implement continuous in a specific env (which one??)
        if behavior_spec.is_action_discrete() == True:
            self.env.action_space = spaces.Discrete(behavior_spec.action_shape[0])

        print(f"Converted Action Space: {self.env.action_space}", flush=True)

        res = Serializer.serializeMeta(self.env.action_space)

        return res
        
    # see behavior_spec: https://github.com/Unity-Technologies/ml-agents/blob/release_4_docs/docs/Python-API.md#interacting-with-a-unity-environment
    # behavior_spec.observation_shapes is what we need, this is an array of tuples [ (), (), (), ... ] which represents variables? (@TODO: Confirm) (e.g. https://github.com/Unity-Technologies/ml-agents/blob/master/docs/Learning-Environment-Examples.md#basic)
    # @TODO: This sounds as a MultiDiscrete environment (https://github.com/openai/gym/blob/master/gym/spaces/multi_discrete.py) so we map to this currently
    async def sim_observation_space(self) -> object:
        behavior_names = list(self.env.behavior_specs.keys()) # the behavior_names which map to a Behavior Spec with observation_shapes, action_type, action_shape
        behavior_idx = 0 # we currently support only 1 behavior spec! even though Unity can support multiple (@TODO)
        behavior_spec = self.env.behavior_specs[behavior_names[behavior_idx]]

        print(f"Observation Shapes: {behavior_spec.observation_shapes}", flush=True)
        observation_space_n_vec = []

        for i in range(0, len(behavior_spec.observation_shapes)):
          observation_space_n_vec.append(behavior_spec.observation_shapes[i][0]) # Get el 0 from the tuple, containing the size

        print(f"Converted Observation Space: {observation_space_n_vec}", flush=True)

        self.env.observation_space = spaces.MultiDiscrete(observation_space_n_vec)
        res = Serializer.serializeMeta(self.env.observation_space)

        return res

    async def sim_create(self, data) -> None:
        """An actor method to create a sim environment."""
        env_id = data['env_id']
        # seed = data['seed']

        print(f'Creating sim with value {env_id}', flush=True)
        print(f"Current dir: {os.getcwd()}", flush=True)
        try:
            print("[Server] Creating Unity Environment", flush=True)
            self.env = UnityEnvironment(f"{os.getcwd()}/src/Server/Unity/envs/{env_id}/{env_id}")

            print("[Server] Resetting environment already", flush=True)
            self.env.reset() # we need to reset first in Unity

            # self.unity_env = UnityEnvironment("./environments/GridWorld")
            # self.env = gym.make(env_id)

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
        #self.env = gym.wrappers.Monitor(self.env, f'./output/{self.actor_id}', resume=False, force=True, video_callable=v_c)
        #self.env = UnityToGymWrapper(self.unity_environment)

        #defaults to BaseEnv
        self.env = UnityToGymWrapper()

    async def sim_monitor_stop(self) -> None:
        self.env.close()

    async def sim_action_sample(self) -> object:
        action = self.env.action_space.sample()
        return action

    async def sim_step(self, data) -> object:
        action = data['action']

        # Unity requires us to set the action with env.set_actions(behavior_name, action) where action is an array
        behavior_names = list(self.env.behavior_specs.keys()) # the behavior_names which map to a Behavior Spec with observation_shapes, action_type, action_shape
        behavior_idx = 0 # we currently support only 1 behavior spec! even though Unity can support multiple (@TODO)
        behavior_name = behavior_names[behavior_idx]
        self.env.set_actions(behavior_name, np.array([ [ action ] ])) # first dimension = number of agents, second dimension = action?
        self.env.step() # step does not return in Unity

        # Get the DecisionSteps and TerminalSteps
        # -> they both contain: 
        # DecisionSteps: Which agents need an action this step? (Note: contains action masks!)
        # E.g.: DecisionStep(obs=[array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0.], dtype=float32)], reward=-0.01, agent_id=0, action_mask=[array([False, False, False])])
        # TerminalSteps: Which agents their episode ended?
        decision_steps, terminal_steps = self.env.get_steps(behavior_names[behavior_idx])


        # print(decision_steps, flush=True)
        # print(terminal_steps, flush=True)
        # print(decision_steps[0], flush=True)
        # print(terminal_steps[0], flush=True)

        # We support 1 decision step currently, get its observation
        # TODO
        decision_step_idx = 0
        decision_step = decision_steps[decision_step_idx]
        obs, reward, agent_id, action_mask = decision_step

        observation = obs[decision_step_idx]
        reward = float(reward)
        isDone = False
        info = {}

        # @TODO: terminal_steps should be implemented, it requires a reset

        # observation is a ndarray, we need to serialize this
        # therefore, change it to list type which is serializable
        if isinstance(observation, np.ndarray):
            observation = observation.tolist()

        return observation, reward, isDone, info