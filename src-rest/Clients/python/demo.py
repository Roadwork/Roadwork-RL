import sys
import os
from Client import Client

import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger('MyLogger')

DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", 3500)
DAPR_GRPC_PORT = os.getenv("DAPR_GRPC_PORT", 50001)

logging.info(f"==================================================")
logging.info(f"DAPR_PORT_GRPC: {DAPR_GRPC_PORT}; DAPR_PORT_HTTP: {DAPR_HTTP_PORT}")
logging.info(f"==================================================")

client = Client("localhost", DAPR_HTTP_PORT, 'id-rw-server-openai')
client.Init("CartPole-v0")
logging.info("init called")
client.MonitorStart()
logging.info("monitorstart called")
client.Reset()
logging.info("reset called")

actionSpaceSample = client.ActionSpaceSample()
print(f"=============== STEP (action: {actionSpaceSample}) ===============")
stepRes = client.Step(actionSpaceSample)
print(stepRes)
print(f'IsDone: {stepRes["isDone"]}')

actionSpaceSample = client.ActionSpaceSample()
print(f"=============== STEP (action: {actionSpaceSample}) ===============")
stepRes = client.Step(actionSpaceSample)
print(stepRes)
print(f'IsDone: {stepRes["isDone"]}')

while not stepRes["isDone"]:
    actionSpaceSample = client.ActionSpaceSample()
    stepRes = client.Step(actionSpaceSample)
    print(stepRes)

client.MonitorStop()

print("=============== DONE ===============")