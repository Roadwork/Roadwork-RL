# README

## Compiling OpenAI + Python Client

kubectl delete deployment rw-server-openai
kubectl delete deployment rw-client-openai

kubectl delete deployment rw-client-python
sudo ./Scripts/build.sh Clients/python roadwork/rw-client-python
./Scripts/start.sh rw-client-python

kubectl delete deployment rw-server-openai
sudo ./Scripts/build.sh Servers/OpenAI roadwork/rw-server-openai
./Scripts/start.sh rw-server-openai

./Scripts/get-output-server.sh rw-server-openai /mnt/f/test/output-server

## Compiling Protobuf

```bash
# 1. Compiling Roadwork Protobuf
python -m grpc_tools.protoc --proto_path=../proto/roadwork/ --python_out=proto_compiled/ --grpc_python_out=proto_compiled/ ../proto/roadwork/roadwork.proto

# 2. Compiling Dapr
python -m grpc_tools.protoc --proto_path=../proto/dapr/ --python_out=proto_compiled/ --grpc_python_out=proto_compiled/ ../proto/dapr/dapr.proto
python -m grpc_tools.protoc --proto_path=../proto/dapr/ --python_out=proto_compiled/ --grpc_python_out=proto_compiled/ ../proto/dapr/daprclient.proto
```