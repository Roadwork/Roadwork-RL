# NGINX Ingress Controller Setup with Dapr

### Prerequistes

- A working kubernetes cluster with Dapr installed
- RoadWork application deployed to the cluster

### Deploy NGINX Ingress Controller with Dapr

We are going to “Daprize” the NGINX Ingress Controller so traffic flows as shown in the following picture:

![/assets/dapr-nginx-ingress.png](./assets/dapr-nginx-ingress.png)

```bash
# Add helm repo of kubernetes-charts
helm repo add stable https://kubernetes-charts.storage.googleapis.com/

# Install ingress controller using helm
helm install nginx stable/nginx-ingress -f Server/dapr-annotations.yaml -n default

```

### Setup TLS termination with certificate

```bash
# Generate certificate using openssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=roadwork/O=roadwork"

# Create kubernetes secret store and add these certs on the store
kubectl create secret tls tls-secret --key tls.key --cert tls.cert

```
> Note: Here certificate are created locally from where we deploy the service. But for production use it should be generated with CA.

### Deploy ingress rule

```bash
# Apply the ingress yaml in kubernetes which use the secret store created in previous step
kubectl apply -f Server/ingress.yaml

```

### Test the application

```bash
# Find the external public IP of the ingress service
kubectl get service --selector=app=nginx-ingress,component=controller -o jsonpath='{.items[*].status.loadBalancer.ingress[0].ip}'

# For minikube/local setup external IP will not be available. Try below commnd to get the URL for that.
  minikube service nginx-nginx-ingress-controller

# Sample curl request to test the application
curl -k -H "Host: roadwork" "https://<external_IP>:<secure_port(443)>/v1.0/actors/ActorOpenAI/roadwork-0-0/method/SimCreate"

# Or make a Postman Put call with below details
  #Url: https://<external_IP>:<secure_port(443)>/v1.0/actors/ActorOpenAI/roadwork-0-0/method/SimCreate
  #Header: {'Host': 'roadwork'}
  #body: { "env_id": "CartPole-v1" }

# If everything runs as expected you should get the following result with status code 200:
null
```
