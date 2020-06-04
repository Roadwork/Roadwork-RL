#!/bin/bash
SERVER_NAME=$1
OUTPUT_DIR=$2 # Where to put the output files in
CURRENT_DIR=$(pwd)
SERVER_PATH="$CURRENT_DIR/Servers/$SERVER_NAME"

export ROADWORK_OUTPUT_DIR=$OUTPUT_DIR

# Install Dependencies
echo "Installing Dependencies"
pip install -r $SERVER_PATH/requirements.txt

# Run Server
echo "Running Server: $SERVER_NAME"
xvfb-run -s "-screen 0 1400x900x24" python3 "$SERVER_PATH/server.py"