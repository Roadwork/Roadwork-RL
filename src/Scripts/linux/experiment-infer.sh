#!/bin/bash
LANGUAGE_NAME=$1 # E.g. python
EXPERIMENT_NAME=$2 # E.g. cartpole
CURRENT_DIR=$(pwd)
EXPERIMENT_PATH="$CURRENT_DIR/Clients/$LANGUAGE_NAME/experiments/$EXPERIMENT_NAME"

# Install Dependencies
echo "Installing Dependencies"
pip install -r $EXPERIMENT_PATH/requirements.txt > /dev/null

# Run Experiment
echo "Running Experiment: $EXPERIMENT_PATH/infer.py"
python3 "$EXPERIMENT_PATH/infer.py"