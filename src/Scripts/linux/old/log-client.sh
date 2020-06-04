#!/bin/bash
if [ -z $1 ]; then
  echo "Usage: ./log.sh <NAME>"
  echo "Example: ./log.sh demo-grpc-server"
  exit 1
fi


NAME=$1

echo "Fetching Logs..."

# Log (note: tail=1000 since -1 doesn't work properly)
echo "=================== DAPR Logs ===================="
kubectl logs p-$NAME -c daprd --tail=1000

echo "================= CONTAINER Logs ================="
kubectl logs -f p-$NAME -c c-$NAME --tail=1000
