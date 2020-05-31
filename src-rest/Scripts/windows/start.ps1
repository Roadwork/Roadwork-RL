$EXECUTION_PATH=(Get-Location).Path
# $PSScriptRoot

$CONTAINER_PATH=$args[0]
$CONTAINER_IMAGE=$args[1]
$DEPLOYMENT_NAME="$CONTAINER_IMAGE"

$DOCKER_REGISTERY="roadwork.io"
$DOCKER_IMAGE="${CONTAINER_IMAGE}:latest"

echo "Cleaning up old resources"
echo "- Removing Deployment"
kubectl delete deployment $DEPLOYMENT_NAME

echo "Creating new deployment"
kubectl create -f $CONTAINER_PATH/kubernetes.yaml.

echo "Deployment Created"
kubectl get deployments $DEPLOYMENT -w