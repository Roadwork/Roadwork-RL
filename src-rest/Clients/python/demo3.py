import os

import grpc

import proto_compiled.dapr_pb2 as dapr_messages
import proto_compiled.dapr_pb2_grpc as dapr_services

from google.protobuf.any_pb2 import Any

from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger('MyLogger')


# Start a gRPC client
port = os.getenv('DAPR_GRPC_PORT')
channel = grpc.insecure_channel(f"localhost:{port}")
client = dapr_services.DaprStub(channel)
print(f"Started gRPC client on DAPR_GRPC_PORT: {port}")

data = Any(value='ACTION=1'.encode('utf-8'))
logger.info(f"[Client][DaprInvoke][debug] Creating Envelope {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
envelope = dapr_messages.InvokeServiceEnvelope(id="openai-server", method="debug", data=data)
logger.info(f"[Client][DaprInvoke][debug] Creating Envelope 2 {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
response = client.InvokeService(envelope)
logger.info(f"[Client][DaprInvoke][debug] Creating Envelope 3 {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
print(response.data.value)

channel.close()