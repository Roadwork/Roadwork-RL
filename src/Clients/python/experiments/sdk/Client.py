import os
import grpc
import sys

import proto_compiled.roadwork_pb2 as roadwork_messages
import proto_compiled.roadwork_pb2_grpc as roadwork_services
import proto_compiled.dapr_pb2 as dapr_messages
import proto_compiled.dapr_pb2_grpc as dapr_services

from google.protobuf.any_pb2 import Any

import protobuf_helpers

from datetime import datetime

class Client:
    def __init__(self, simId, envId):
        self.simId = simId
        self.envId = envId

    def DaprInvoke(self, method, req, res_type):
        envelope = dapr_messages.InvokeServiceEnvelope(id=self.simId, method=method, data=protobuf_helpers.to_any_pb(req))
        res = self.client.InvokeService(envelope)
        res = protobuf_helpers.from_any_pb(res_type, res.data)
        return res
    
    def Init(self, host, port):
        self.host = host
        self.port = port
        print(f"Trying to connect on {self.host}:{self.port}")
        self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")
        self.client = dapr_services.DaprStub(self.channel)
        print(f"Started gRPC client on DAPR_GRPC_PORT: {self.port}")
        req = roadwork_messages.CreateRequest(envId=self.envId)
        res = self.DaprInvoke("create", req, roadwork_messages.CreateResponse)

        self.instanceId = res.instanceId

    def Reset(self):
        req = roadwork_messages.ResetRequest(instanceId=self.instanceId)
        res = self.DaprInvoke("reset", req, roadwork_messages.ResetResponse)
        return res.observation

    def ActionSpaceSample(self):
        req = roadwork_messages.ActionSpaceSampleRequest(instanceId=self.instanceId)
        res = self.DaprInvoke("action-space-sample", req, roadwork_messages.ActionSpaceSampleResponse)
        return res.action

    def ActionSpaceInfo(self):
        req = roadwork_messages.ActionSpaceInfoRequest(instanceId=self.instanceId)
        res = self.DaprInvoke("action-space-info", req, roadwork_messages.ActionSpaceInfoResponse)
        return res.result

    def ObservationSpaceInfo(self):
        req = roadwork_messages.ObservationSpaceInfoRequest(instanceId=self.instanceId)
        res = self.DaprInvoke("observation-space-info", req, roadwork_messages.ObservationSpaceInfoResponse)
        return res.result

    def Step(self, action):
        req = roadwork_messages.StepRequest(instanceId=self.instanceId, action=action)
        res = self.DaprInvoke("step", req, roadwork_messages.StepResponse)
        return res

    def MonitorStart(self):
        req = roadwork_messages.BaseRequest(instanceId=self.instanceId)
        res = self.DaprInvoke("monitor-start", req, roadwork_messages.BaseResponse)
        return res

    def MonitorStop(self):
        req = roadwork_messages.BaseRequest(instanceId=self.instanceId)
        res = self.DaprInvoke("monitor-stop", req, roadwork_messages.BaseResponse)
        return res