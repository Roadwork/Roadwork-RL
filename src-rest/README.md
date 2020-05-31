
**Server**
./Scripts/windows/build.ps1 ./Servers/OpenAI/ rw-server-openai
./Scripts/windows/start-server.ps1 ./Servers/OpenAI/ rw-server-openai

**Client**
./Scripts/windows/build.ps1 ./Clients/python/experiments/cartpole rw-client-python-cartpole
./Scripts/windows/start-client.ps1 ./Clients/python/experiments/cartpole rw-client-python-cartpole