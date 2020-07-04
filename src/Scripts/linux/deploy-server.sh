#!/bin/bash

if [ -z $1 -o -z $2 ]; then
  echo "Usage: ./build.sh <DOCKER_FILE_LOCATION> <NAME>"
  echo "Example: ./build.sh Server/ roadwork/sim-server"
  exit 1
fi

DOCKER_FILE_LOCATION=$1
DOCKER_IMAGE="$2:latest"

cd $DOCKER_FILE_LOCATION

docker build -t $DOCKER_IMAGE .