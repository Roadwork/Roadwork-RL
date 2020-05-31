import os
import sys
import requests

from datetime import datetime

import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger('MyLogger')

class Client:
    def __init__(self, host, port, serverId):
        self.host = host
        self.port = port
        self.serverId = serverId
        self.url = f"http://{host}:{port}/v1.0/invoke/{serverId}"
    
    def Init(self, simId):
        self.simId = simId
        self.Create()

    def Create(self):
        msg = { "envId": self.simId }
        res = requests.post(f"{self.url}/method/create", json=msg)
        res = res.json()
        self.instanceId = res["instanceId"]

    def Reset(self):
        res = requests.post(f"{self.url}/method/{self.instanceId}/reset")
        res = res.json()
        return res

    def ActionSpaceSample(self):
        res = requests.post(f"{self.url}/method/{self.instanceId}/action-space-sample")
        res = res.json()
        return res

    def ActionSpaceInfo(self):
        res = requests.post(f"{self.url}/method/{self.instanceId}/action-space-info")
        res = res.json()
        return res

    def ObservationSpaceInfo(self):
        res = requests.post(f"{self.url}/method/{self.instanceId}/observation-space-info")
        res = res.json()
        return res

    def Step(self, action):
        msg = { "action": action }
        res = requests.post(f"{self.url}/method/{self.instanceId}/step", json=msg)
        res = res.json()
        return res

    def MonitorStart(self):
        res = requests.post(f"{self.url}/method/{self.instanceId}/monitor-start")
        return res

    def MonitorStop(self):
        res = requests.post(f"{self.url}/method/{self.instanceId}/monitor-stop")
        return res

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