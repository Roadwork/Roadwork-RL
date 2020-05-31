$EXECUTION_PATH=(Get-Location).Path
# $PSScriptRoot

$CONTAINER_PATH=$args[0]
$CONTAINER_IMAGE=$args[1]
$DEPLOYMENT_NAME="$CONTAINER_IMAGE"
$ROADWORK_SERVER_OUTPUT_PATH="C:\\roadwork\\$DEPLOYMENT_NAME"

$DOCKER_REGISTERY="roadwork.io"
$DOCKER_IMAGE="${CONTAINER_IMAGE}:latest"

echo "Creating Server Output Folder"
if (!(Test-Path $ROADWORK_SERVER_OUTPUT_PATH -PathType Container)) {
    New-Item -ItemType Directory -Force -Path $ROADWORK_SERVER_OUTPUT_PATH
}

echo "Cleaning up old resources"
echo "- Removing Deployment"
kubectl delete deployment $DEPLOYMENT_NAME

echo "Creating new deployment"
kubectl create -f $CONTAINER_PATH/kubernetes.yaml.

echo "Deployment Created"
# kubectl get deployments $DEPLOYMENT -w

$POD=kubectl get pods -l app=$DEPLOYMENT_NAME --output=jsonpath='{.items[*].metadata.name}'
echo "Opening Logs for pod $POD"

Do
{
    $POD=kubectl get pods -l app=$DEPLOYMENT_NAME --output=jsonpath='{.items[*].metadata.name}'
    $res=kubectl get pods $POD --output=jsonpath='{.status.phase}'
    echo "Awaiting Pod to Start, Current status: $res"
    Start-Sleep -Seconds 1
} While (!($res -eq "Running"))

kubectl logs -f $POD -c server