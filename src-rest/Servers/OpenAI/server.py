import flask
from flask import request, jsonify
from flask_cors import CORS
import sys
import os
import logging
import time
from concurrent import futures
from datetime import datetime

# Import OpenAI
from OpenAIEnv import Envs

import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger('MyLogger')

APP_HTTP_PORT = os.getenv('APP_HTTP_PORT', 9000)
DAPR_HTTP_PORT = os.getenv('DAPR_HTTP_PORT', 3500)
DAPR_GRPC_PORT = os.getenv('DAPR_GRPC_PORT', 50001) # Note: currently 50001 is always default

logger.info(f"==================================================")
logger.info(f"DAPR_PORT_GRPC: {DAPR_GRPC_PORT}; DAPR_PORT_HTTP: {DAPR_HTTP_PORT}")
logger.info(f"==================================================")

# import gym
envs = Envs()

app = flask.Flask(__name__)
CORS(app)

# /step/<instanceId> will give def met(instanceId)
@app.route('/create', methods=['POST'])
def create():
    envId = request.json["envId"]
    instanceId = envs.create(envId)

    res = {
        "instanceId": instanceId
    }

    print(f"Created instance {instanceId} for sim environment {envId}")
    
    return jsonify(res)

@app.route('/<instanceId>/reset', methods=['POST'])
def reset(instanceId):
    res = envs.reset(instanceId)
    return jsonify(res)

@app.route('/<instanceId>/action-space-sample', methods=['POST'])
def actionSpaceSample(instanceId):
    res = envs.get_action_space_sample(instanceId)
    return jsonify(res)

@app.route('/<instanceId>/action-space-info', methods=['POST'])
def actionSpaceInfo(instanceId):
    res = envs.get_action_space_info(instanceId)
    return jsonify(res)

@app.route('/<instanceId>/observation-space-info', methods=['POST'])
def observationSpaceInfo(instanceId):
    res = envs.get_observation_space_info(instanceId)
    return jsonify(res)

@app.route('/<instanceId>/step', methods=['POST'])
def step(instanceId):
    action = request.json["action"]

    step = envs.step(instanceId, action, True)

    res = {
        "obs": step[0],
        "reward": step[1],
        "isDone": step[2],
        "info": step[3]
    }

    return jsonify(res)

@app.route('/<instanceId>/monitor-start', methods=['POST'])
def monitorStart(instanceId):
    res = envs.monitor_start(instanceId, '/mnt/roadwork', True, False, 10)
    return jsonify(res)

@app.route('/<instanceId>/monitor-stop', methods=['POST'])
def monitorStop(instanceId):
    envs.monitor_close(instanceId)
    return jsonify({})

if __name__ == '__main__':
    logger.info(f'Running on port {APP_HTTP_PORT}')
    app.run(host="0.0.0.0", port=APP_HTTP_PORT)