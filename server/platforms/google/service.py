# -*- encoding: UTF-8 -*-

import google.oauth2.credentials
import google_auth_oauthlib.flow

import flask

class GoogleService:
    def __init__(self, credentials):
        self.service = self.create_service(credentials)

    def create_service(self, creds):
        raise("Not Implemented")
