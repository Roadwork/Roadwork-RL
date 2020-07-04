#!/bin/bash
SERVER_NAME=$1
OUTPUT_DIR=$2 # Where to put the output files in
CURRENT_DIR=$(pwd)
SERVER_PATH="$CURRENT_DIR/Servers/$SERVER_NAME"

if [ -z $1 -o -z $2 ]; then
  echo "Usage: $0 <SERVER_NAME> OUTPUT_DIR"
  echo "Example: $0 OpenAI ./output/server"
  exit 1
fi

export ROADWORK_OUTPUT_DIR=$OUTPUT_DIR

# Install Dependencies
echo "Installing Dependencies"
pip install -r $SERVER_PATH/requirements.txt > /dev/null

# Run Server
echo "Running Server: $SERVER_NAME"
echo "- Output Directory: $ROADWORK_OUTPUT_DIR"
xvfb-run -s "-screen 0 1400x900x24" python3 "$SERVER_PATH/server.py"

# xvfb-run -e /tmp/xvfb.err -a -s "-screen 0 1400x900x24 +extension RANDR" -- glxinfo
