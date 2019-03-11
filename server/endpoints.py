# -*- encoding: UTF-8 -*-

import os

from .middlewares import login_required
from flask import Flask, json, g, request
from db.service import Service
from flask_cors import CORS

import server.platforms.utils.util as util

app = Flask(__name__)
CORS(app)


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.yaml')
config = util.load_yaml(CONFIG_PATH)


@app.route("/sessions", methods=["GET"])
@login_required
def index():
    return json_response(Service(config['mongo']).get_recent_sessions())


@app.route("/session/<int:created_at>", methods=["GET"])
@login_required
def show(created_at):
    return json_response(Service(config['mongo']).get_session(created_at))


@app.route("/presenter/<username>", methods=["GET"])
@login_required
def presenter(username):
    return json_response(Service(config['mongo']).get_presenter(username))

def json_response(payload, status=200):
    return (json.dumps(payload), status, {'content-type': 'application/json'})
