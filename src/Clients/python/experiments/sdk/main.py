import sys
import os
from Client import Client

DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", 3500)
DAPR_GRPC_PORT = os.getenv("DAPR_GRPC_PORT", 50001)

print(f"==================================================")
print(f"DAPR_PORT_GRPC: {DAPR_GRPC_PORT}; DAPR_PORT_HTTP: {DAPR_HTTP_PORT}")
print(f"==================================================")

print("Opening Client")
client = Client('id-rw-server-openai', 'CartPole-v0')
client.Init("localhost", DAPR_GRPC_PORT)
client.MonitorStart()
client.Reset()

print("Action Space Info")
print(client.ActionSpaceInfo())

print("Observation Space Info")
print(client.ObservationSpaceInfo())

actionSpaceSample = client.ActionSpaceSample()
print(f"=============== STEP (action: {actionSpaceSample}) ===============")
stepRes = client.Step(actionSpaceSample)
print(stepRes)
print(f'IsDone: {stepRes.isDone}')

actionSpaceSample = client.ActionSpaceSample()
print(f"=============== STEP (action: {actionSpaceSample}) ===============")
stepRes = client.Step(actionSpaceSample)
print(stepRes)
print(f'IsDone: {stepRes.isDone}')

while not stepRes.isDone:
    actionSpaceSample = client.ActionSpaceSample()
    stepRes = client.Step(actionSpaceSample)
    print(stepRes)

client.MonitorStop()

print("=============== DONE ===============")