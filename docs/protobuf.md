# Protobuf

Protobuf is being used to serialize a state in a compact way, so it can be transferred over a medium to be used by another language. Allowing us to interact with simulators in a bi-directional way from any language that implements these Protocol buffers.

## Generating Protobuf 

### Python

In the root of the Simulator project run (e.g. in OpenAI/):

```bash
python -m grpc_tools.protoc --proto_path=../proto/ --python_out=grpc_compiled/ --grpc_python_out=grpc_compiled/ ../proto/dapr.proto
python -m grpc_tools.protoc --proto_path=../proto/ --python_out=grpc_compiled/ --grpc_python_out=grpc_compiled/ ../proto/daprclient.proto
```

> Latest proto at: https://github.com/dapr/dapr/tree/master/pkg/proto

python -m grpc_tools.protoc --proto_path=../../proto/ --python_out=grpc_compiled/ --grpc_python_out=grpc_compiled/ ../../proto/dapr.proto
python -m grpc_tools.protoc --proto_path=../../proto/ --python_out=grpc_compiled/ --grpc_python_out=grpc_compiled/ ../../proto/daprclient.proto




python -m grpc_tools.protoc --proto_path=../../protobuf-definitions/ --python_out=. --grpc_python_out=. ../../protobuf-definitions/services/simulator.proto
