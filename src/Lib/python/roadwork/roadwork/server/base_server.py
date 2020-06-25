import grpc
import time
import uuid

from abc import ABC, abstractmethod
from concurrent import futures
import gym.spaces.utils as gym_utils

from roadwork.proto import api_v1, api_service_v1
from roadwork.grpc import Unserializer
from roadwork.grpc import Serializer
from roadwork.utils import ProtoUtil

# Should normally implement api_service_v1.RoadworkServicer
class Server(ABC):
    def __init__(self, sim_id, port):
        self.observation_space_info = None
        self.action_space_info = None
        self.port = port
        self.sim_id = sim_id
        self.instance_id = "%s-%s-%s" % ("roadwork", sim_id, str(uuid.uuid4().hex)[:8])
        return

    def start(self):
        # Create a gRPC server
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
        api_service_v1.add_RoadworkServicer_to_server(self, self.server)

        # Start the gRPC server
        print(f'[Server] Created Server with InstanceID: {self.instance_id}')
        print(f'[Server] Listening on port {self.port}.')
        self.server.add_insecure_port(f'[::]:{self.port}')
        self.server.start()

        # Since server.start() doesn't block, we need to do a sleep loop
        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            print(f'[Server] KeyboardInterrupt, stopping server.')
            self.server.stop(0)

    # ====================================================================================
    # Required to be implemented
    # ====================================================================================
    @abstractmethod
    def get_action_space_info(self):
        pass

    @abstractmethod
    def get_observation_space_info(self):
        pass

    @abstractmethod
    def action_space_sample(self):
        pass

    @abstractmethod
    def create(self, env_id, seed):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def step(self, action, is_render):
        pass

    # ====================================================================================
    # gRPC Abstraction
    # ====================================================================================
    def ActionSpaceSample(self, request, context):
        print("[Server] Action Sample")
        action = self.action_space_sample()

        # Make sure it's a list
        if isinstance(action, (int)):
            action = [ action ]
        elif isinstance(action, (list, tuple)) or ('numpy' in str(type(action))):
            try:
                action = action.tolist()
            except TypeError:
                print(type(action))
                print('TypeError')

        # Return
        res = api_v1.ActionSpaceSampleResponse(action=action)
        return res

    def ActionSpaceInfo(self, request, context):
        print("[Server] Action Space Info")
        action_space = Serializer.serializeMeta(self.action_space_info)
        res = api_v1.ActionSpaceInfoResponse(result=action_space)
        return res

    def ObservationSpaceInfo(self, request, context):
        print("[Server] Observation Space Info")
        observation_space = Serializer.serializeMeta(self.observation_space_info)
        res = api_v1.ObservationSpaceInfoResponse(result=observation_space)
        return res

    def Create(self, request, context):
        print(f"[Server] Create Sim: {request.envId}")

        # Create our env
        self.create(request.envId, seed = 0)

        # Once it's created, also get observation and action space
        self.action_space_info = self.get_action_space_info()
        self.observation_space_info = self.get_observation_space_info()

        # Return response
        res = api_v1.CreateResponse(instanceId=self.instance_id)

        return res

    def Reset(self, request, context):
        print("[Server] Reset")
        observation = self.reset()
        res = api_v1.ResetResponse(observation=observation)
        return res

    def Step(self, request, context): # StepRequest
        print("[Server] Step")

        # Unserialize Actions based on action_space
        action = Unserializer.unserializeAction(self.action_space_info, request.actions)

        # Take step
        observation, reward, isDone, info = self.step(action, request.render)

        # Flatten this so we can send over wire
        observation = gym_utils.flatten(self.observation_space_info, observation) # @todo: res_osi should be cached

        # Encode Info (sometimes it can contain a bool)
        info = ProtoUtil.json_object_to_proto_map(info)
        res = api_v1.StepResponse(reward=reward, isDone=isDone, info=info, observation=observation)

        return res
    
    def Render(self, request, context):
        print("[Server] Render")
        return

    def Close(self, request, context):
        print("[Server] Close")
        return

    def MonitorStart(self, request, context): # BaseResponse
        print("[Server] Monitor Start")
        # envs.monitor_start(request.instanceId, OUTPUT_DIRECTORY, True, False, 10) # Log to local dir so we can reach it
        res = api_v1.BaseResponse()
        return res

    def MonitorStop(self, request, context): # BaseResponse
        print("[Server] Monitor Stop")
        # envs.monitor_close(request.instanceId)
        res = api_v1.BaseResponse()
        return res




# @abstractmethod
# def create(simId):
#     pass

# @abstractmethod
# def step(instanceId, actions, is_render):
#     pass
    


# def Step(self, request, context): # StepRequest
#     # Unserialize Actions based on action_space
#     actions = Unserializer.unserializeAction(self.action_space, request.actions)

#     # Take step
#     observation, reward, isDone, info = self.step(request.instanceId, actions, request.render)

#     # Flatten this so we can send over wire
#     observation = gym_utils.flatten(self.observation_space, observation) # @todo: res_osi should be cached

#     # Encode Info (sometimes it can contain a bool)
#     info = ProtoUtil.json_object_to_proto_map(info)
#     res = api_v1.StepResponse(reward=reward, isDone=isDone, info=info, observation=observation)
    
#     return res

# def Reset(self, request, context): # ResetResponse
#     res = api_v1.ResetResponse(observation=envs.reset(request.instanceId))
#     return res

# def Render(self, request, context):
#     return

# def Close(self, request, context):
#     return

# def ActionSpaceSample(self, request, context): # ActionSpaceSampleResponse
#     res = api_v1.ActionSpaceSampleResponse(actions=envs.get_action_space_sample(request.instanceId))
#     return res

# def ActionSpaceInfo(self, request, context): # ActionSpaceInfoResponse
#     res = api_v1.ActionSpaceInfoResponse(result=envs.get_action_space_info(request.instanceId))
#     return res

# def ObservationSpaceInfo(self, request, context): # ObservationSpaceInfoResponse
#     info = envs.get_observation_space_info(request.instanceId)
#     res = api_v1.ObservationSpaceInfoResponse(result=info)
#     return res

# def MonitorStart(self, request, context): # BaseResponse
#     envs.monitor_start(request.instanceId, OUTPUT_DIRECTORY, True, False, 10) # Log to local dir so we can reach it
#     res = api_v1.BaseResponse()
#     return res

# def MonitorStop(self, request, context): # BaseResponse
#     envs.monitor_close(request.instanceId)
#     res = api_v1.BaseResponse()
#     return res
