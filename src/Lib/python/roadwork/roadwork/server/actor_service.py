# -*- coding: utf-8 -*-
# Copyright (c) Roadwork
# Licensed under the MIT License.

from flask import Flask, jsonify
from roadwork.flask_dapr.actor import DaprActor

from dapr.conf import settings

class RoadworkActorService:
    def __init__(self):
        self.app = Flask(f'{RoadworkActorService.__name__}Service')

        # Enable DaprActor Flask extension
        self.actor = DaprActor(self.app)

        # Register Default Actors provided by Roadwork
        # actor.register_actor(RoadworkActor)

        # # Show that it's working
        # @self.app.route('/')
        # def index():
        #     return jsonify({'status': 'ok'}), 200

    def register(self, actor):
        self.actor.register_actor(actor)
        print(f"Registered Actor: '{actor.__name__}'")

    def start(self):
        port = settings.HTTP_APP_PORT
        print(f"Starting server on port {port}")
        self.app.run(port=port)