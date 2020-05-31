#!/bin/bash

if [ -z $1 ]; then
  echo "Usage: ./start.sh <NAME>"
  echo "Example: ./start.sh demo-grpc-server"
  exit 1
fi

NAME=$1
DIRECTORY=`dirname $0`


# @todo: when deployment exists, run kubectl -n service rollout restart deployment <deployment>
# this way we don't delete the old deployment
# note: another solution might be to scale down and up again (https://medium.com/faun/how-to-restart-kubernetes-pod-7c702ca984c1)

echo "Deleting old deployment..."
kubectl delete deployment $NAME
echo "Creating deployment..."
kubectl apply -f ./Deploy/$NAME.yaml

sleep 3 # It's still processing the deployment recreate

echo "Opening logs"
$DIRECTORY/log-client.sh $NAME