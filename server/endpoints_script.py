# -*- encoding: UTF-8 -*-

import os
from datetime import datetime

import google.oauth2.credentials
import google_auth_oauthlib.flow

from middlewares import login_required
from flask import Flask, json, g, request, session, url_for, redirect
from db.service import Service
from flask_cors import CORS

import platforms.utils.util as util
from scripts.data_sync import DataSync
from workflow.tasks.whitepaper_journal.event_poster import WhitepaperJournalEventPoster

app = Flask(__name__)
app.secret_key = 'Octopus: Star of Smart Media'
CORS(app)

AUTHORIZE_URL = "https://blockchainabc.org:4433/authorize_google"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.yaml')
config = util.load_yaml(CONFIG_PATH)


@app.route("/googleredirect", methods=["GET"])
def google_callback():
    settings = config['google']
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings['creds_file'], scopes=settings['scopes'], state=state)
    flow.redirect_uri = url_for('google_callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    service = Service(config['mongo'])
    existing = service.get_credential_by_token(credentials.token)
    if existing:
        credential_id = str(existing['_id'])
    else:
        credential_id = service.create_session({
            'createdAt': datetime.utcnow(),
            'source': 'google',
            'credentials': {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }
        })
    sep = '?' if len(state.split('?')) == 1 else '&'
    params = '{}credential_id={}'.format(sep, credential_id)
    return redirect(state + params)


@app.route("/authorize_google", methods=["GET"])
def authorize():
    settings = config['google']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings['creds_file'], scopes=settings['scopes'])
    flow.redirect_uri = url_for('google_callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        state=request.args.get('origin_url'),
        include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)


@app.route("/revoke_google", methods=["GET"])
@login_required
def revoke(session_id):
    if 'credentials' not in session:
        return json_response({'success': True})
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])
    revoke = request.post('https://accounts.google.com/o/oauth2/revoke',
        params={'token': credentials.token},
        headers = {'content-type': 'application/x-www-form-urlencoded'})
    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return json_response({'success': True})
    else:
        return json_response({'success': False})


@app.route("/clear_google", methods=["GET"])
@login_required
def clear():
    if 'credentials' in session:
        del session['credentials']
    return json_response({'success': True})


@app.route("/refresh", methods=["POST"])
@login_required
def refresh():
    DataSync(config).sync()
    return json_response({'success': True})


@app.route("/schedule", methods=["POST"])
@login_required
def schedule():
    return json_response({'success': True})


@app.route("/event_poster/<int:session_id>", methods=["GET"])
@login_required
def event_poster(session_id):
    credential_id = request.args.get('credential_id', '')
    if not credential_id:
        return json_response({
            'success': False, 'authorize_url': AUTHORIZE_URL})
    credential = Service(config['mongo']).get_credential(credential_id)
    creds = google.oauth2.credentials.Credentials(
        **credential['credentials'])
    poster_generator = WhitepaperJournalEventPoster(creds)
    poster_generator.process(session_id)
    return json_response({'success': True})


@app.route("/sessions", methods=["GET"])
@login_required
def index():
    return json_response(Service(config['mongo']).get_recent_sessions())


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
