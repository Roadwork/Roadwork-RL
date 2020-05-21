#!/usr/bin/env python3
import uuid
import gym
import numpy as np
import six
import argparse
import sys
import json

# import Serializer

import logging
logger = logging.getLogger('werkzeug')
logger.setLevel(logging.ERROR)

########## Error handling ##########
class InvalidUsage(Exception):
    status_code = 400
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

########## Container for environments ##########
class Envs(object):
    """
    Container and manager for the environments instantiated
    on this server.

    When a new environment is created, such as with
    envs.create('CartPole-v0'), it is stored under a short
    identifier (such as '3c657dbc'). Future API calls make
    use of this instance_id to identify which environment
    should be manipulated.
    """
    def __init__(self):
        self.envs = {}
        self.id_len = 8

    def _lookup_env(self, instance_id):
        try:
            return self.envs[instance_id]
        except KeyError:
            raise InvalidUsage('Instance_id {} unknown'.format(instance_id))

    def _remove_env(self, instance_id):
        try:
            del self.envs[instance_id]
        except KeyError:
            raise InvalidUsage('Instance_id {} unknown'.format(instance_id))

    def create(self, env_id, seed=None):
        try:
            env = gym.make(env_id)
            if seed:
                env.seed(seed)
        except gym.error.Error:
            raise InvalidUsage("Attempted to look up malformed environment ID '{}'".format(env_id))
        except Exception as e:
            raise Exception(e)

        instance_id = str(uuid.uuid4().hex)[:self.id_len]
        self.envs[instance_id] = env
        return instance_id

    def list_all(self):
        return dict([(instance_id, env.spec.id) for (instance_id, env) in self.envs.items()])

    def reset(self, instance_id):
        env = self._lookup_env(instance_id)
        obs = env.reset()
        return env.observation_space.to_jsonable(obs)

    def step(self, instance_id, action, render):
        env = self._lookup_env(instance_id)
        if isinstance( action, six.integer_types ):
            nice_action = action
        else:
            nice_action = np.array(action)
        if render:
            env.render()
        [observation, reward, done, info] = env.step(nice_action)
        obs_jsonable = env.observation_space.to_jsonable(observation)
        return [obs_jsonable, reward, done, info]

    def get_action_space_contains(self, instance_id, x):
        env = self._lookup_env(instance_id)
        return env.action_space.contains(int(x))

    def get_action_space_info(self, instance_id):
        env = self._lookup_env(instance_id)
        return env.action_space
        # return self._get_space_properties(env.action_space)

    def get_action_space_sample(self, instance_id):
        env = self._lookup_env(instance_id)
        action = env.action_space.sample()
        if isinstance(action, (list, tuple)) or ('numpy' in str(type(action))):
            try:
                action = action.tolist()
            except TypeError:
                logger.error(type(action))
                logger.error('TypeError')
        return action

    def get_observation_space_contains(self, instance_id, j):
        env = self._lookup_env(instance_id)
        # info = self._get_space_properties(env.observation_space)
        info = env.observation_space
        for key, value in j.items():
            # Convert both values to json for comparibility
            if json.dumps(info[key]) != json.dumps(value):
                print('Values for "{}" do not match. Passed "{}", Observed "{}".'.format(key, value, info[key]))
                return False
        return True

    def get_observation_space_info(self, instance_id):
        env = self._lookup_env(instance_id)
        return env.observation_space
        # return self._get_space_properties(env.observation_space)

    # # A space is an object that can consist out of sub objects
    # def _get_space_properties(self, space):
    #     return Serializer.serialize(space)

    def monitor_start(self, instance_id, directory, force, resume, video_callable):
        env = self._lookup_env(instance_id)
        if video_callable == False:
            v_c = lambda count: False
        else:
            v_c = lambda count: count % video_callable == 0
        self.envs[instance_id] = gym.wrappers.Monitor(env, directory, force=force, resume=resume, video_callable=v_c) 

    def monitor_close(self, instance_id):
        env = self._lookup_env(instance_id)
        env.close()

    def env_close(self, instance_id):
        env = self._lookup_env(instance_id)
        env.close()
        self._remove_env(instance_id)