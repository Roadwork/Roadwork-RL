# Roadwork RL in Kubernetes

## Prerequisites

> **Note:** Click the links for more information on how to install

1. Install Kubernetes cluster
2. [Install kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
3. [Install helm 3](https://helm.sh/docs/intro/install/)
4. [Docker Hub Account](https://hub.docker.com)

## Setting up Dapr

### Install Dapr via Helm

```bash
kubectl create ns dapr-system
helm install dapr dapr/dapr --set-string global.tag=edge --namespace dapr-system
```

### Installing Redis state store

#### 1. Deploying Redis to the Kubernetes Cluster

```bash
# Create Redis on Kubernetes
# Note: in namespace "statestore"
kubectl create ns statestore
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install redis bitnami/redis --namespace statestore

# Get the password
echo "Password: $(kubectl get secret --namespace statestore redis -o jsonpath="{.data.redis-password}" | base64 --decode)"
```

#### 2. Creating the Redis State store YAML for Dapr

Once Redis has been deployed, we need to configure Dapr to utilize it correctly. For that, follow these steps:

1. Clone the `src/Server/redis.example.yaml` file to `src/Server/redis.yaml` with `cp src/Server/redis.example.yaml src/Server/redis.yaml`
2. Open the created YAML file situated in `src/Server/redis.yaml`
3. Configure the Redis YAML with the password from above
4. Install this YAML to the Kubernetes cluster with `kubectl apply -f ./src/Server/redis.yaml`

> **Note:** When applied, you will see the output `component.dapr.io/statestore created`. You can also check `kubectl get components.dapr.io` to ensure that the statestore has been created.

## Installing Roadwork-RL Simulation Cluster

### Deploy Roadwork-RL to Kubernetes

```bash
# Navigate to the <ROADWORK>/src/Server folder
cd <ROOT REPO>/src/Server

# Start Server
kubectl apply -f kubernetes.yaml

# Ensure rw-server is running (should show rw-server-*-* with status Running and Ready 2/2)
kubectl get pods

# Get Logs
kubectl logs -f deployment/rw-server -c server -f
```

### Scale out Roadwork-RL Server

```bash
# Get the deployment name
kubectl get deployment

# Scale it out with the amount of replicas you want
kubectl scale --replicas=<instance number> deployment rw-server
```

### Delete Roadwork-RL Deployment

```bash
kubectl delete deployment rw-server
```

## Running an Experiment on the Simulation Cluster

Roadwork RL provides two ways to run experiments on Kubernetes. If your kubernetes resource is enough to train the model, you can deploy experiments to cluster. Otherwise, experiments can be run on the workstation.

### Python

> Note: This is the experimental setup. For production purpose, you need to have Domain and SSL cert.

1. Deploy the [nginx ingress controller with Dapr](/docs/getting-started/nginx-ingress-controller-setup.md) in the Kubernetes cluster.
2. Execute `kubectl get service --selector=app=nginx-ingress,component=controller -o jsonpath='{.items[*].status.loadBalancer.ingress[0].ip}'` to get the service IP address which we can connect to over HTTP(S)
3. Run the experiment as shown below

```bash
# Configure the Roadwork Simulation Cluster IP Address to run the Experiment against
# E.g. export ROADWORK_SERVER_URL=https://20.190.28.131:443
# E.g. export ROADWORK_SERVER_URL=https://127.0.0.1:33843
export ROADWORK_SERVER_URL=https://<EXTERNAL-IP>

# Navigate to your experiment folder
cd <REPO ROOT>/src/Experiments/rllib/cartpole

# Execute your experiment
python3 train.py
```

### As a Docker container

Here is the example to deploy [rllib/cartpole](../../src/experiments/rllib/cartpole/) to cluster:

```bash
cd <REPO ROOT>/src/Experiments/rllib/cartpole

# Build Docker Image
docker build -t <your docker registry>/rw-exp-rllib-cartpole:latest .
docker push <your docker registry>/rw-exp-rllib-cartpole:latest

# Deploy Experiment
kubectl apply -f kubernetes.yaml
```

