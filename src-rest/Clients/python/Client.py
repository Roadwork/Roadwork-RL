import os
import sys
import requests

from datetime import datetime

class Client:
    def __init__(self, host, port, serverId, simId):
        self.host = host
        self.port = port
        self.serverId = serverId
        self.simId = simId
        self.url = f"http://{host}/v1.0/invoke/{serverId}"
    
    def Init(self):
        self.Create()

    def Create(self):
        msg = { "envId": self.simId }
        response = requests.post(f"{self.url}/method/create", json=msg)
        print(response)
        self.instanceId = response.instanceId

    def Reset(self):
        msg = { "instanceId": self.simId }
        res = requests.post(f"{self.url}/method/reset", json=msg)
        return res

    # def ActionSpaceSample(self):
    #     req = roadwork_messages.ActionSpaceSampleRequest(instanceId=self.instanceId)
    #     res = self.DaprInvoke("action-space-sample", req, roadwork_messages.ActionSpaceSampleResponse)
    #     return res.action

    # def ActionSpaceInfo(self):
    #     req = roadwork_messages.ActionSpaceInfoRequest(instanceId=self.instanceId)
    #     res = self.DaprInvoke("action-space-info", req, roadwork_messages.ActionSpaceInfoResponse)
    #     return res

    # def ObservationSpaceInfo(self):
    #     req = roadwork_messages.ObservationSpaceInfoRequest(instanceId=self.instanceId)
    #     res = self.DaprInvoke("observation-space-info", req, roadwork_messages.ObservationSpaceInfoResponse)
    #     return res

    # def Step(self, action):
    #     req = roadwork_messages.StepRequest(instanceId=self.instanceId, action=action)
    #     res = self.DaprInvoke("step", req, roadwork_messages.StepResponse)
    #     return res

    def MonitorStart(self):
        msg = { "instanceId": self.simId }
        res = requests.post(f"{self.url}/method/monitor-start", json=msg)
        return res

    # def MonitorStop(self):
    #     req = roadwork_messages.BaseRequest(instanceId=self.instanceId)
    #     res = self.DaprInvoke("monitor-stop", req, roadwork_messages.BaseResponse)
    #     return res

    # def DebugSlow(self):
    #     req = roadwork_messages.BaseRequest(instanceId=self.instanceId)
    #     res = self.DaprInvoke("debug", req, roadwork_messages.BaseResponse)
    #     return res

    # def DebugFast(self):
    #     data = Any(value='ACTION 1'.encode('utf-8'))
    #     print(f"[Client][DaprInvoke][debug] Creating Envelope {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
    #     envelope = dapr_messages.InvokeServiceEnvelope(id=self.simId, method="debug", data=data)
    #     print(f"[Client][DaprInvoke][debug] Creating Envelope 2 {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
    #     res = self.client.InvokeService(envelope)
    #     print(f"[Client][DaprInvoke][debug] Creating Envelope 3 {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
    #     return res