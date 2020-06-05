# Tests

## Running

pytest -s --disable-pytest-warnings

## Compiling Protobuf

python -m grpc_tools.protoc --proto_path=../src/proto/roadwork/ --python_out=proto_compiled/ --grpc_python_out=proto_compiled/ ../src/proto/roadwork/roadwork.proto
