# Python SDK

## Generating Protobuf

```bash
python3 -m grpc_tools.protoc --proto_path=../../protobuf-definitions/ --python_out=. --grpc_python_out=. ../../protobuf-definitions/services/simulator.proto
```