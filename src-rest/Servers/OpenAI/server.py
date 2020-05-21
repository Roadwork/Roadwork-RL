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

@app.route('/create', methods=['POST'])
def create():
    [envId] = request.json

    res = dict()
    res['instanceId'] = envs.create(envId)

    logger.info('Received something')

    return jsonify(res)

@app.route('/reset', methods=['POST'])
def reset():
    [instanceId] = request.json

    res = dict()
    res['observation'] = envs.reset(instanceId)

    return jsonify(res)

@app.route('/action-space-sample', methods=['POST'])
def actionSpaceSample():
    [instanceId] = request.json

    res = dict()
    res['action'] = envs.get_action_space_sample(instanceId)

    return jsonify(res)

@app.route('/action-space-info', methods=['POST'])
def actionSpaceInfo():
    [instanceId] = request.json

    res = dict()
    res['observation'] = envs.get_action_space_info(instanceId)

    return jsonify(res)

@app.route('/observation-space-info', methods=['POST'])
def observationSpaceInfo():
    [instanceId] = request.json

    res = dict()
    res['result'] = envs.reset(instanceId)

    return jsonify(res)

@app.route('/step', methods=['POST'])
def step():
    [instanceId, action, render] = request.json

    res = dict()
    res['result'] = envs.step(instanceId, action, render)

    return jsonify(res)

@app.route('/monitor-start', methods=['POST'])
def monitorStart():
    [instanceId] = request.json

    res = dict()
    res['result'] = envs.monitor_start(instanceId, './monitor', True, False, 10)

    return jsonify(res)

@app.route('/monitor-stop', methods=['POST'])
def monitorStop():
    [instanceId] = request.json

    envs.monitor_close(instanceId)
    res = dict()

    return jsonify(res)

if __name__ == '__main__':
    logger.info(f'Running on port {APP_HTTP_PORT}')
    app.run(host="0.0.0.0", port=APP_HTTP_PORT)