# Roadwork-RL through Dapr - Work in progress

## Architecture

![](../assets/roadwork-rl-abstraction.png)
![](../assets/roadwork-rl-cluster.png)

## Debug


## Installation

For fresh install the following steps were followed:

```bash
# 1. Dapr Install
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
> https://github.com/dapr/docs/blob/master/getting-started/environment-setup.md

sudo dapr init

# 2. Dapr Dev Python install
# Note: 3.7 is required for Asyncio.run to be available
git clone https://github.com/dapr/python-sdk.git
modify setup.cfg and change > 3.8 to > 3.7
pip install -e

# 3. Dependencies (Gym, Dapr Actor and Roadwork)
sudo apt-get install ffmpeg python-opengl xvfb
sudo pip3 install gym
sudo pip3 install flask
sudo pip3 install -r dev-requirements.txt # in src-dapr/
sudo pip3 install nest-asyncio
sudo pip3 install stable-baselines # client only
sudo pip3 install tensorflow==1.14.0

# 4. Install Roadwork Library
cd src/Lib/python/roadwork
sudo pip install -e .
```

## Running

You can now run an experiment, for that following these steps:

```bash
# 1. Start X Server for rendering
sudo Xvfb -screen 0 1024x768x24 &
export DISPLAY=:0

# 2. Navigate to Dapr Folder
cd src-dapr

# 3. Run Main Server (containing OpenAI)
sudo dapr run --app-id demo-actor --app-port 3000 python3 ./main.py

# 4. Run Experiment (in different window, also in src-dapr folder)
sudo dapr run --app-id demo-client python3 ./Experiments/baselines/cartpole/train.py
```

## PyPi

```bash
# Deploying package
./Scripts/windows/deploy-python-package.ps1
```

## Kubernetes

### Server

#### 1. Installing Redis

```bash
# Install Helm
# https://helm.sh/docs/intro/install/
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh

# Install redis into cluster
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install redis bitnami/redis

echo "Redis is now running, credentials:"
echo "Host: redis-master:6379"
echo "Password: $(kubectl get secret --namespace default redis -o jsonpath="{.data.redis-password}" | base64 --decode)"
```

#### 2. Installing Server

```bash
# Build Server
./Scripts/linux/build-server.sh Server/ roadwork.io/sim-server

# Remove old Server
kubectl delete deployment rw-server

# Start Server
kubectl apply -f Server/kubernetes.yaml

# Get Logs
kubectl logs -f deployment/rw-server -c server -f
```

### Client

```bash
# Build Client
./Scripts/linux/build-client.sh Experiments/baselines/cartpole roadwork.io/rw-exp-baselines-cartpole

# Remove old Client
kubectl delete pod p-rw-exp-cartpole

# Start Client
kubectl apply -f Experiments/baselines/cartpole/kubernetes.yaml

# Get Logs
kubectl logs pod/p-rw-exp-cartpole -c experiment -f
```