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
    def __init__(self, simId, envId):
        self.simId = simId
        self.envId = envId

    def Init(self, host, port):
        self.host = host
        self.port = port
        print(f"Trying to connect on {self.host}:{self.port}")
        self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")
        self.client = api_service_v1.RoadworkStub(self.channel)
        print(f"Started gRPC client on GRPC_PORT: {self.port}")
        req = api_v1.CreateRequest(envId=self.envId)
        res = self.client.Create(req)

        self.instanceId = res.instanceId
        
        print("Getting Action Space")
        self.action_space = self.ActionSpaceInfo()

        print("Getting Observation Space")
        self.observation_space = self.ObservationSpaceInfo()
        print(self.observation_space)

    def Reset(self):
        req = api_v1.ResetRequest(instanceId=self.instanceId)
        res = self.client.Reset(req)
        return np.array(res.observation)

    def ActionSpaceSample(self):
        req = api_v1.ActionSpaceSampleRequest(instanceId=self.instanceId)
        res = self.client.ActionSpaceSample(req)
        return res.action

    def ActionSpaceInfo(self):
        req = api_v1.ActionSpaceInfoRequest(instanceId=self.instanceId)
        res = self.client.ActionSpaceInfo(req)
        return Unserializer.unserializeMeta(res.result)

    def ObservationSpaceInfo(self):
        req = api_v1.ObservationSpaceInfoRequest(instanceId=self.instanceId)
        res = self.client.ObservationSpaceInfo(req)
        return Unserializer.unserializeMeta(res.result)

    def Step(self, actions):
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

    def MonitorStart(self):
        req = api_v1.BaseRequest(instanceId=self.instanceId)
        res = self.client.MonitorStart(req)
        return res

    def MonitorStop(self):
        req = api_v1.BaseRequest(instanceId=self.instanceId)
        res = self.client.MonitorStop()
        return res