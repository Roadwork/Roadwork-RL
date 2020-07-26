# Roadwork RL

> **Note:** This project is currently under heavy development and may change. It should not be used for production deployments yet.

Roadwork-RL is a Reinforcement Learning Platform that aims to act as an abstraction layer between the actual simulator integration and the algorithm acting on it. Its goal is to reduce the complexity required to spin up experiments that require a horizontally and isolated scaled simulator. It allows researchers to focus on the Reinforcement Learning algorithms.

## Architecture

A high-level architecture of the platform can be found below. The focus points of Roadwork-RL are:
* Code agnostic platform, allowing clients in different languages
* Easy simulator integrations
* The OpenAI Gym language

![/assets/roadwork-rl-abstraction.png](./assets/roadwork-rl-abstraction.png)

## Getting Started

You can get started yourself in 2 different ways, for researchers we recommend "**Kubernetes**" while as for development purposes, we recommend running the "**Standalone**" installation. See the links below for the different Operating Systems to get started.

> **Note:** We recommend Linux as the target Operating System

* [Windows](./docs/getting-started/windows.md) - WIP
* [Linux](./docs/getting-started/linux.md)

Once the installation is done, you can run your first experiment (Cartpole) through the following commands:

```bash
# 0a. Start X Server for rendering
sudo Xvfb -screen 0 1024x768x24 &
export DISPLAY=:0

# 0b. Navigate to Roadwork
cd ~/roadwork-rl

# 1. Start Server
sudo dapr run --app-id rw-server --app-port 3000 python3 ./src/Server/main.py

# 2. Start Experiment (different window)
sudo dapr run --app-id demo-client python3 ./src/Experiments/baselines/cartpole/train.py
```

### Language SDKs Available

* [Python](./docs/sdk/python.md)
* [NodeJS](./docs/sdk/node.md) - WIP

### Simulators Implemented

* [OpenAI](https://github.com/openai/gym)

## References

* [High-Level Technical Overview](./docs/technical.md)
* [Protobuf Serialization](./docs/protobuf.md)
* [Spaces](./docs/spaces.md)
* [Simulators](./docs/simulators.md)
* [grpc.io](https://grpc.io)
* [Protobuf](https://github.com/protocolbuffers/protobuf)
* [Dapr](https://github.com/dapr/dapr)
* [Kubernetes](https://github.com/kubernetes/kubernetes)

## TODO

- [ ] Integrate [Facebook ReAgent](https://github.com/facebookresearch/ReAgent) on top of this
    * Simulation Observation Downloader
    * Trainer On-Policy & Off-Policy
- Add more simulators
  - [ ] [Unity ML-Agents](https://github.com/Unity-Technologies/ml-agents)
  - [ ] [Project Malmo](https://www.microsoft.com/en-us/research/project/project-malmo/)
- [ ] Performance Benchmarks (what is the impact of this library compared to a vanilla implemented)
* Create a custom language for state describing
    * Currently we can describe a state as shown before: `Tuple([ Box(0, 255, shape=(64, 64, 3)), Box(-50, 50, shape=(3, )) ])`. This might be too abstract or language dependent and could be done easier + more efficient. E.g. think of a Robotic arm, where we should be able to describe each join independently.