import os

import grpc
import proto_compiled.dapr_pb2 as dapr_messages
import proto_compiled.dapr_pb2_grpc as dapr_services
import proto_compiled.roadwork_pb2 as roadwork_messages

from google.protobuf.any_pb2 import Any

# Start a gRPC client
port = os.getenv('DAPR_GRPC_PORT')
channel = grpc.insecure_channel(f"localhost:{port}")
client = dapr_services.DaprStub(channel)
print(f"Started gRPC client on DAPR_GRPC_PORT: {port}")

# Invoke the Receiver
data = Any(value='SOME_DATA'.encode('utf-8'))
response = client.InvokeService(dapr_messages.InvokeServiceEnvelope(id="openai-server", method="my_method", data=data))

# Unpack the response
res = roadwork_messages.ActionSpaceSampleResponse()
response.data.type_url = "type.googleapis.com/roadwork.ActionSpaceSampleResponse"
response.data.Unpack(res)

# Print Result
print(res)

channel.close() 