# -*- encoding: UTF-8 -*-

import os
import json
import logging
from datetime import datetime

import google.oauth2.credentials
import google_auth_oauthlib.flow

from middlewares import login_required
from flask import Flask, json, g, request, session, url_for, redirect
from db.service import Service
from flask_cors import CORS

import platforms.utils.util as util
from scripts.data_sync import DataSync
from workflow.tasks.membership.sync import MemberSync
from workflow.tasks.whitepaper_journal.event_poster import WhitepaperJournalEventPoster

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('endpoint')
logger.setLevel(logging.INFO)

app = Flask(__name__)
app.secret_key = 'Octopus: Star of Smart Media'
CORS(app)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.yaml')
config = util.load_yaml(CONFIG_PATH)

mongo_service = Service(config['mongo'])


def load_google_creds():
    query_res = mongo_service.get_credential(g.user, 'google')
    if not query_res:
        return None
    cred = query_res['credentials']
    return google.oauth2.credentials.Credentials(
        token=cred['token'],
        id_token=cred['id_token'],
        scopes=cred['scopes'])


@app.route("/store_google_creds", methods=["POST"])
@login_required
def store_google_creds():
    data = json.loads(request.data.decode('utf8'))
    mongo_service.create_credential({
        'created_at': datetime.utcnow(),
        'source': 'google',
        'user': g.user,
        'credentials': {
            'token': data['access_token'],
            'id_token': data['id_token'],
            'scopes': data['scope'].split(' ')
        }
    })
    return json_response({'success': True})


@app.route("/refresh_events", methods=["GET"])
@login_required
def sync_events():
    credentials = load_google_creds()
    if not credentials:
        return json_response({'success': False, 'error': 'Google Not Authorized'})
    DataSync(credentials, config['mongo']).sync()
    return json_response({'success': True})


@app.route("/sessions", methods=["GET"])
@login_required
def load_sessions():
    mongo_service = Service(config['mongo'])
    recent_sessions = mongo_service.get_recent_sessions()
    candidate_sessions = mongo_service.get_candidate_sessions()
    return json_response(recent_sessions + candidate_sessions)


@app.route("/members", methods=["GET"])
@login_required
def load_members():
    members = Service(config['mongo']).get_members()
    return json_response(members)


@app.route("/refresh_members", methods=["GET"])
@login_required
def sync_members():
    credentials = load_google_creds()
    if not credentials:
        return json_response({'success': False, 'error': 'Google Not Authorized'})
#    MemberSync(credentials, config['mongo']).sync()
    MemberSync(credentials,
        config['imgur']['creds_file'],
        config['mongo']).sync_membership_card()
    return json_response({'success': True})


@app.route("/schedule", methods=["POST"])
@login_required
def schedule():
    return json_response({'success': True})


@app.route("/event_poster/<int:session_id>", methods=["GET"])
@login_required
def event_poster(session_id):
    credentials = load_google_creds()
    if not credentials:
        return json_response({'success': False, 'error': 'Google Not Authorized'})
    poster_generator = WhitepaperJournalEventPoster(credentials)
    poster_generator.process(session_id)
    return json_response({'success': True})


@app.route("/session/<int:session_id>", methods=["GET"])
@login_required
def show(session_id):
    return json_response(Service(config['mongo']).get_session(session_id))


@app.route("/presenter/<username>", methods=["GET"])
@login_required
def presenter(username):
    return json_response(Service(config['mongo']).get_presenter(username))


def json_response(payload, status=200):
    return (json.dumps(payload), status, {'content-type': 'application/json'})


if __name__ == "__main__":
    app.run(host='0.0.0.0',port='4433',
            ssl_context=('/root/cert/blockchainabc.org.crt', '/root/cert/blockchainabc.org.key'),
            threaded=True, debug=True)
