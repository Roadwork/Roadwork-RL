import sys
import os
import logging
import time
from concurrent import futures
from datetime import datetime

import grpc

# Custom Protobuf
import proto_compiled.roadwork_pb2 as roadwork_messages # Contains Message Classes
import proto_compiled.roadwork_pb2_grpc as roadwork_grpc # Contains Server & Client Classes

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
class RoadworkServicer(roadwork_grpc.RoadworkServicer):
    def Create(self, request, context): # CreateRequest
        res = roadwork_messages.CreateResponse(instanceId=envs.create(request.envId))
        return res

    def Step(self, request, context): # StepRequest
        # Returns 0 = obs_jsonable, 1 = reward, 2 = done, 3 = info in object (e.g. {'TimeLimit.truncated': True})
        res_step = envs.step(request.instanceId, request.action, request.render)

        # Observation Space
        res_osi = envs.get_observation_space_info(request.instanceId)
        space_wrapper = roadwork_messages.SpaceWrapper()

        if res_osi.HasField('discrete'):
            space_discrete = roadwork_messages.SpaceDiscrete()
            space_discrete.observation = res_step[0]
            space_wrapper.discrete.CopyFrom(space_discrete)
        elif res_osi.HasField('box'):
            space_box = roadwork_messages.SpaceBox()
            space_box.observation.extend(res_step[0])
            space_wrapper.box.CopyFrom(space_box)
        else:
            logging.error("Unsupported Space Type: %s" % res_step[3]['name'])
            logging.error(info)

        # Encode Info (sometimes it can contain a bool)
        info = ProtoUtil.json_object_to_proto_map(res_step[3])
        res = roadwork_messages.StepResponse(reward=res_step[1], isDone=res_step[2], info=info, observation=space_wrapper)
        
        return res

    def Reset(self, request, context): # ResetResponse
        res = roadwork_messages.ResetResponse(observation=envs.reset(request.instanceId))
        return res

    def Render(self, request, context):
        return

    def Close(self, request, context):
        return

    def ActionSpaceSample(self, request, context): # ActionSpaceSampleResponse
        res = roadwork_messages.ActionSpaceSampleResponse(action=envs.get_action_space_sample(request.instanceId))
        return res

    def ActionSpaceInfo(self, request, context): # ActionSpaceInfoResponse
        res = roadwork_messages.ActionSpaceInfoResponse(result=envs.get_action_space_info(request.instanceId))
        return res

    def ObservationSpaceInfo(self, request, context): # ObservationSpaceInfoResponse
        res = roadwork_messages.ObservationSpaceInfoResponse(result=envs.get_observation_space_info(request.instanceId))
        return res

    def MonitorStart(self, request, context): # BaseResponse
        envs.monitor_start(request.instanceId, OUTPUT_DIRECTORY, True, False, 10) # Log to local dir so we can reach it
        res = roadwork_messages.BaseResponse()
        return res

    def MonitorStop(self, request, context): # BaseResponse
        envs.monitor_close(request.instanceId)
        res = roadwork_messages.BaseResponse()
        return res

    # print(f"[OnInvoke][{request.method}] Done @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")

# Create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
roadwork_grpc.add_RoadworkServicer_to_server(RoadworkServicer(), server)

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