# Roadwork RL in Kubernetes

## Prerequisites

1. Install Kubernetes cluster
2. [Install kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
3. [Install helm 3](https://helm.sh/docs/intro/install/)
4. [Docker Hub Account](https://hub.docker.com)

## Set up Dapr

### Install Dapr via Helm

```bash
kubectl create ns dapr-system
helm install dapr dapr/dapr --set-string global.tag=edge --namespace dapr-system
```

### Installing Redis state store

1. Deploy Redis to your cluster:

```bash
kubectl create ns statestore
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install redis bitnami/redis --namespace statestore

echo "Password: $(kubectl get secret --namespace default redis -o jsonpath="{.data.redis-password}" | base64 --decode)"
```

2. Create redis state store yaml

> Please refer to [redis config template](../../src/Server/redis.yaml) and update password.

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: default
spec:
  type: state.redis
  metadata:
  - name: redisHost
    value: redis-master.statestore.svc.cluster.local:6379
  - name: redisPassword
    value: <Password>
  - name: actorStateStore
    value: "true"
```

3. Apply redis statestore yaml

```bash
$ kubectl apply -f ./redis.yaml
```

Ensure that statestore config is applied:

```bash
$ kubectl get components.dapr.io
NAME         AGE
statestore   7h1m
```

## Install RoadWork Server

### Deploy RoadWork RL server client

```bash
$ cd <ROOT REPO>/src/Server

# Start Server
$ kubectl apply -f kubernetes.yaml

# Ensure rw-server is running
$ kubectl get pods
NAME                                                   READY   STATUS              RESTARTS   AGE
...
rw-server-dd467659f-4mk4k                              2/2     Running             0          5h12m
...

# Get Logs
$ kubectl logs -f deployment/rw-server -c server -f
```

### Scale out Roadwork RL server client

```bash
$ kubectl get deployment
NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE
rw-server                             5/5     5            5           6h18m

$ kubectl scale --replicas=<instance number> deployment rw-server
```

### Delete Roadwork rl deployment

```bash
kubectl delete deployment rw-server
```

## Run Experiment client

Roadwork RL provides two ways to run experiments on Kubernetes. If your kubernetes resource is enough to train model,
you can deploy experiments to cluster. Otherwise, experiments can be run on workstation.

### Deploy experiment client to cluster

Here is the example to deploy [rllib/cartpole](../../src/experiments/rllib/cartpole/) to cluster:

```bash
cd <REPO ROOT>/src/Experiments/rllib/cartpole

# Build Docker Image
docker build -t <your docker registry>/rw-exp-rllib-cartpole:latest .
docker push <your docker registry>/rw-exp-rllib-cartpole:latest

# Deploy Experiment
kubectl apply -f kubernetes.yaml
```

### Run experiments outside cluster

1. Deploy [nginx ingress controller with Dapr](./nginx-ingress-controller-setup.md) in Kubernetes cluster.

> Note: This is the experimental setup. For production purpose, you need to have Domain and SSL cert.

1. Get nginx-nginx-ingress-controller EXTERNAL-IP address

```bash
$ kubectl get svc
NAME                                  TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)                               AGE
nginx-nginx-ingress-controller        LoadBalancer   10.0.252.177   20.190.28.131   80:31019/TCP,443:31414/TCP            7h17m
```

3. Run Experiment

```bash
cd <REPO ROOT>/src/Experiments/rllib/cartpole

# Set roadwork server url environment variable with EXTERNAL-IP
export ROADWORK_SERVER_URL=https://<EXTERNAL-IP>

# test server example
# export ROADWORK_SERVER_URL=https://20.190.28.131:443

python3 train.py
```
