import os
import grpc
import sys
import numpy as np
import grpc

import gym.spaces.utils as gym_utils

# Roadwork
import roadwork.proto.roadwork_pb2 as api_v1
import roadwork.proto.roadwork_pb2_grpc as api_service_v1
from roadwork.grpc import Unserializer


from google.protobuf.any_pb2 import Any
from datetime import datetime

class Client:
    metadata = { 'render.modes': [ 'human' ] }

    def __init__(self, simId, envId):
        self.simId = simId
        self.envId = envId

    def init(self, host, port):
        self.host = host
        self.port = port
        print(f"[Roadwork][Client] Trying to connect on {self.host}:{self.port}")
        self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")
        self.client = api_service_v1.RoadworkStub(self.channel)
        print(f"[Roadwork][Client] Started gRPC client on GRPC_PORT: {self.port}")
        req = api_v1.CreateRequest(envId=self.envId)
        res = self.client.Create(req)

        self.instanceId = res.instanceId
        
        print("[Roadwork][Client] Getting Action Space")
        self.action_space = self._action_space_info()

        print("[Roadwork][Client] Getting Observation Space")
        self.observation_space = self._observation_space_info()

        print("[Roadwork][Client] Initialization Done")

    def _observation_space_info(self):
        req = api_v1.ObservationSpaceInfoRequest(instanceId=self.instanceId)
        res = self.client.ObservationSpaceInfo(req)
        return Unserializer.unserializeMeta(res.result)

    def observation_space_info(self):
        return self.observation_space

    def _action_space_info(self):
        req = api_v1.ActionSpaceInfoRequest(instanceId=self.instanceId)
        res = self.client.ActionSpaceInfo(req)
        return Unserializer.unserializeMeta(res.result)
    
    def action_space_info(self):
        return self.action_space

    def reset(self):
        req = api_v1.ResetRequest(instanceId=self.instanceId)
        res = self.client.Reset(req)
        return np.array(res.observation)

    def action_space_sample(self):
        req = api_v1.ActionSpaceSampleRequest(instanceId=self.instanceId)
        res = self.client.ActionSpaceSample(req)
        return res.action

    def step(self, actions):
        # Make sure actions is a list
        if isinstance(actions, np.ndarray):
            actions = actions.tolist()
        elif not isinstance(actions, list):
            actions = [ actions ]

        req = api_v1.StepRequest(instanceId=self.instanceId, actions=actions)
        res = self.client.Step(req)

        reward = res.reward
        done = res.isDone
        obs = gym_utils.unflatten(self.observation_space, res.observation)
        info = {} # @TODO, convert Protobuf map<string, string> to Dict

        return [ obs, reward, done, info ]

    def monitor_start(self):
        req = api_v1.BaseRequest(instanceId=self.instanceId)
        res = self.client.MonitorStart(req)
        return res

    def monitor_stop(self):
        req = api_v1.BaseRequest(instanceId=self.instanceId)
        res = self.client.MonitorStop()
        return res