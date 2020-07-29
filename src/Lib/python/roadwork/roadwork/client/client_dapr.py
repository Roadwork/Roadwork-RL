import os
import grpc
import sys
import numpy as np
import grpc
import requests
import time

import gym.spaces.utils as gym_utils

# Roadwork
from roadwork.json import Unserializer

import uuid

#asgiref

class ClientDapr:
    metadata = { 'render.modes': [ 'human' ] }

    def __init__(self, simId):
        self.simId = simId
        self.actor_id = "%s-%s-%s" % ("roadwork", self.simId, str(uuid.uuid4().hex)[:8])
        self.client_session = requests.Session()

        dapr_http_port = os.environ.get('DAPR_HTTP_PORT', 3500)
        self._default_url = f'http://localhost:{dapr_http_port}/v1.0/actors/{self.simId}/{self.actor_id}/method'

    def _create(self, envId):
        self.client_session.post(f'{self._default_url}/SimCreate', json={ 'env_id': envId })
        self.action_space = self._action_space_info()
        self.observation_space = self._observation_space_info()
    
    def _reset(self):
        r = self.client_session.post(f'{self._default_url}/SimReset', data='')
        return r.json()
    
    def _action_space_sample(self):
        r = self.client_session.post(f'{self._default_url}/SimActionSample', data='')
        return r.json()

    def _step(self, action):
        if type(action) == np.int64:
            action = int(action)

        if isinstance(action, np.ndarray):
            action = action.tolist()

        for _ in range(0, 3):
            try:
                r = self.client_session.post(f'{self._default_url}/SimStep', json={ 'action': action })
                obs, reward, done, info = r.json()
                return [ obs, reward, done, info ]
            except Exception as ex:
                print (repr(ex), flush=True)
                time.sleep(1)
        return []

    def _monitor_start(self, episode_interval):
        self.client_session.post(f'{self._default_url}/SimMonitorStart', json={ 'episode_interval': episode_interval })
    
    def _monitor_stop(self):
        self.client_session.post(f'{self._default_url}/SimMonitorStop', data='')

    def _sim_call_method(self, method, *method_args, **method_kwargs):
        r = self.client_session.post(f'{self._default_url}/SimCallMethod', json={ 
            'method': method,
            'args': method_args,
            'kwargs': method_kwargs
        })
        res = r.json()

        if isinstance(res, list):
            res = res[0] # @todo: assumption is that list gets wrapped again? and then returns one big list, causing us to take element idx 0. But not sure

        return res

    def set_state(self, key, value):
        self.client_session.post(f'{self._default_url}/SimSetState', json={ 'key': key, 'value': value })

    def get_state(self, key):
        r = self.client_session.post(f'{self._default_url}/SimGetState', json={ 'key': key })
        return r.json()

    def _observation_space_info(self):
        r = self.client_session.post(f'{self._default_url}/SimObservationSpace', data='')
        observation_space = r.json()
        observation_space = Unserializer.unserializeMeta(observation_space)
        return observation_space

    def _action_space_info(self):
        r = self.client_session.post(f'{self._default_url}/SimActionSpace', data='')
        action_space = r.json()
        action_space = Unserializer.unserializeMeta(action_space)
        return action_space

    def create(self, envId, **kwargs):
        self._create(envId, **kwargs)

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
