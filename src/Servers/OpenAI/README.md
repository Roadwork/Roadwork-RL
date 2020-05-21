Running Example:

cd src-dapr/Simulators/OpenAI
dapr run --app-id openai-server --protocol grpc --app-port 50051 python .\server.py

cd src-dapr/SDKs/python
dapr run --app-id demo-client --protocol grpc python demo.py