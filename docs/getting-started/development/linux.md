# Installation - Linux

## Standalone Installation

### Installing Python 3.7

```bash
# Install Python 3.7
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.7 -y

# Set Python 3.7 as our default
sudo update-alternatives --config python3
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1

# Relink
sudo rm /usr/bin/python3
sudo ln -s /usr/bin/python3.7 /usr/bin/python3

# Install Pip (also for sudo)
curl -s https://bootstrap.pypa.io/get-pip.py | python3
sudo curl -s https://bootstrap.pypa.io/get-pip.py | sudo python3
```

> **Note:** Check with `sudo python3 --version` to see if the correct version is installed

### Platform Installation

```bash
# Install dependencies
sudo apt install -y --no-install-recommends apt-utils build-essential curl xvfb ffmpeg xorg-dev libsdl2-dev swig cmake python-opengl dos2unix

# Install Docker
sudo apt install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
# sudo apt install docker-ce docker-ce-cli containerd.io
sudo apt install docker.io -y

# Install Dapr (https://github.com/dapr/docs/blob/master/getting-started/environment-setup.md)
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash

# Navigate to home dir
cd ~

# Install Dapr python SDK
sudo pip3 install dapr-ext-fastapi-dev

# Clone Roadwork
cd ~
git clone https://github.com/roadwork/roadwork-rl

# Install Roadwork Python SDK
cd ~/roadwork-rl/src/Lib/python/roadwork
sudo pip3 install -e .

# Install requirements Server
cd ~/roadwork-rl/src/Server
sudo pip3 install -r requirements.txt

# Install requirements Cartpole Experiment
cd ~/roadwork-rl/src/Experiments/baselines/cartpole
sudo pip3 install -r requirements.txt

# Init Dapr
sudo dapr init
```

### Temporary: Patching Daprd to edge version

We need to have daprd running on the edge version (see `sudo dapr --version`), since it has a fix we require for the platform. Sadly enough this is a manual patch, seeing that GitHub doesn't allow artifact downloading by guests (e.g. https://api.github.com/repos/dapr/dapr/actions/artifacts/12021957/zip).

1. Download the latest artifact from https://github.com/dapr/dapr/actions/runs/180628900
2. Unzip until you get daprd as a binary
3. Copy daprd to /usr/local/bin and replace the old one
4. Run `sudo dapr --version` and confirm that you see: `Runtime version: edge`

### Starting the Server

Once the installation is done, you can now start the Server as follows:

```bash
# 0a. Start X Server for rendering
sudo Xvfb -screen 0 1024x768x24 &
export DISPLAY=:0

# 0b. Navigate to Roadwork-RL Server
cd <REPO ROOT>/src/Server

# 1. Start Server
sudo dapr run --app-id rw-server --app-port 3000 -- uvicorn --port 3000 main:app

# 2. Start OpenAI Experiment (different window)
sudo dapr run --app-id demo-client python3 ./src/Experiments/baselines/cartpole/train.py

# 3. Start ML-Agent Experiment (different window)
sudo dapr run --app-id demo-client python3 ./src/Experiments/baselines/cartpole-agent/train.py
```