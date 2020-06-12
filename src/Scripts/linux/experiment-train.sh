#!/bin/bash
LANGUAGE_NAME=$1 # E.g. python
EXPERIMENT_NAME=$2 # E.g. cartpole
CURRENT_DIR=$(pwd)
EXPERIMENT_PATH="$CURRENT_DIR/Clients/$LANGUAGE_NAME/experiments/$EXPERIMENT_NAME"

if [ -z $1 -o -z $2 ]; then
  echo "Usage: $0 <LANGUAGE_NAME> <EXPERIMENT_NAME>"
  echo "Example: $0 python baselines/cartpole"
  exit 1
fi

# Install Dependencies
echo "Installing Dependencies"
pip install -r $EXPERIMENT_PATH/requirements.txt > /dev/null

# Run Experiment
echo "Running Experiment: $EXPERIMENT_PATH/train.py"
python3 "$EXPERIMENT_PATH/train.py"