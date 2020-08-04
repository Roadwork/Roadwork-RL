# Minikube

## Installation

```bash
# Check if virtualization is supported (should NOT be empty)
grep -E --color 'vmx|svm' /proc/cpuinfo

# Download Minikube
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
  && chmod +x minikube

# Add it to your path
sudo mkdir -p /usr/local/bin/
sudo install minikube /usr/local/bin/

# Check installation
minikube status
```

## Running a Kubernetes cluster

```bash
# Create a cluster with 4 cpus, 8GB RAM
minikube start --cpus=4 --memory=8196
```

## Useful commands

```bash
# Stopping the cluster
minikube stop

# Starting a previously created cluster
minikube start

# Deleting the cluster
minikube delete

# Viewing status
minikube status

# Viewing Kubernetes dashboard
minikube dashboard
```