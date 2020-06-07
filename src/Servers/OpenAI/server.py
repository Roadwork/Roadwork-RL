import sys
import os
import logging
import time
from concurrent import futures
from datetime import datetime

import gym.spaces.utils as gym_utils

import grpc
import numpy as np
import traceback

# Custom Protobuf
# import proto_compiled.roadwork_pb2 as roadwork_messages # Contains Message Classes
# import proto_compiled.roadwork_pb2_grpc as roadwork_grpc # Contains Server & Client Classes

from roadwork.proto import api_v1, api_service_v1
from roadwork.grpc import Serializer
from roadwork.grpc import Unserializer

import protobuf_helpers

from google.protobuf.any_pb2 import Any

# Import OpenAI
from OpenAIEnv import Envs

APP_PORT_GRPC    = os.getenv('APP_GRPC_PORT',  50050)
OUTPUT_DIRECTORY = os.getenv('ROADWORK_OUTPUT_DIR',  "")

print(f"============================================================")
print(f"APP_PORT_GRPC: {APP_PORT_GRPC}")
print(f"OUTPUT_DIRECTORY: {OUTPUT_DIRECTORY}")
print(f"============================================================")

# import gym
envs = Envs()

class ProtoUtil:
    @staticmethod
    def json_object_to_proto_map(jsonObject):
        info = {}

        for key, value in jsonObject.items():
            if type(value) == bool:
                info[key] = str(int(value)) # Convert bool to 0 or 1
            else:
                info[key] = str(value)
        
        return info


# Our server methods
class RoadworkServicer(api_service_v1.RoadworkServicer):
    def Create(self, request, context): # CreateRequest
        env = envs.create(request.envId)
        print(f"[Server][{env}] Created Environment")

        # action_space = envs.get_action_space_info(env)
        # print(f"[Server][{env}] - Action Space: {action_space}")

        # observation_space = envs.get_observation_space_info(env)
        # print(f"[Server][{env}] - Observation Space: {observation_space}")

        res = api_v1.CreateResponse(instanceId=env)
        return res

    def Step(self, request, context): # StepRequest
        try:
            # Get action space
            action_space = envs.get_action_space_info(request.instanceId)
            actions = Unserializer.unserializeAction(action_space, request.actions)

            # Returns 0 = obs_jsonable, 1 = reward, 2 = done, 3 = info in object (e.g. {'TimeLimit.truncated': True})
            observation, reward, isDone, info = envs.step(request.instanceId, actions, request.render)

            # Get Observation Space Info (gym.spaces)
            res_env = envs._lookup_env(request.instanceId)
            res_osi = res_env.observation_space

            # Flatten this so we can send over wire
            observation = gym_utils.flatten(res_osi, observation) # @todo: res_osi should be cached

            # Encode Info (sometimes it can contain a bool)
            info = ProtoUtil.json_object_to_proto_map(info)
            res = api_v1.StepResponse(reward=reward, isDone=isDone, info=info, observation=observation)
        except:
            print(sys.exc_info())
            traceback.print_tb(sys.exc_info()[2])
            raise
        
        return res

    def Reset(self, request, context): # ResetResponse
        res = api_v1.ResetResponse(observation=envs.reset(request.instanceId))
        return res

    def Render(self, request, context):
        return

    def Close(self, request, context):
        return

    def ActionSpaceSample(self, request, context): # ActionSpaceSampleResponse
        res = api_v1.ActionSpaceSampleResponse(actions=envs.get_action_space_sample(request.instanceId))
        return res

    def ActionSpaceInfo(self, request, context): # ActionSpaceInfoResponse
        res = api_v1.ActionSpaceInfoResponse(result=envs.get_action_space_info(request.instanceId))
        return res

    def ObservationSpaceInfo(self, request, context): # ObservationSpaceInfoResponse
        info = envs.get_observation_space_info(request.instanceId)
        res = api_v1.ObservationSpaceInfoResponse(result=info)
        return res

    def MonitorStart(self, request, context): # BaseResponse
        envs.monitor_start(request.instanceId, OUTPUT_DIRECTORY, True, False, 10) # Log to local dir so we can reach it
        res = api_v1.BaseResponse()
        return res

    def MonitorStop(self, request, context): # BaseResponse
        envs.monitor_close(request.instanceId)
        res = api_v1.BaseResponse()
        return res

    # print(f"[OnInvoke][{request.method}] Done @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")

# Create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
api_service_v1.add_RoadworkServicer_to_server(RoadworkServicer(), server)

# Start the gRPC server
print(f'Starting server. Listening on port {APP_PORT_GRPC}.')
server.add_insecure_port(f'[::]:{APP_PORT_GRPC}')
server.start()

# Since server.start() doesn't block, we need to do a sleep loop
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)