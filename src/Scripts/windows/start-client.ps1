$EXECUTION_PATH=(Get-Location).Path
# $PSScriptRoot

$CONTAINER_PATH=$args[0]
$CONTAINER_IMAGE=$args[1]
$DEPLOYMENT_NAME="$CONTAINER_IMAGE"
# $ROADWORK_OUTPUT_PATH="C:\\roadwork\\$DEPLOYMENT_NAME"

$DOCKER_REGISTERY="roadwork.io"
$DOCKER_IMAGE="${CONTAINER_IMAGE}:latest"

# echo "Creating Output Folder"
# if (!(Test-Path $ROADWORK_OUTPUT_PATH -PathType Container)) {
#     New-Item -ItemType Directory -Force -Path $ROADWORK_OUTPUT_PATH
# }

echo "Cleaning up old resources"
echo "- Removing Job"
kubectl delete job $DEPLOYMENT_NAME

echo "Creating new Job"
kubectl create -f $CONTAINER_PATH/kubernetes.yaml.

echo "Job Created"
# kubectl get jobs $DEPLOYMENT -w

echo "Opening Logs"
$POD=kubectl get pods -l app=rw-client-python-cartpole --output=jsonpath='{.items[*].metadata.name}'

Do
{
    $res=kubectl get pods $POD --output=jsonpath='{.status.phase}'
    echo "Awaiting Pod to Start, Current status: $res"
    Start-Sleep -Seconds 1
} While (!($res -eq "Running"))

kubectl logs -f $POD -c client