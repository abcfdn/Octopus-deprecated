# -*- encoding: UTF-8 -*-

from google.oauth2 import service_account


class GoogleService:
    def __init__(self, settings):
        creds = self.load_creds(settings)
        self.service = self.create_service(creds)

    def create_service(self, creds):
        raise("Not Implemented")

    def load_creds(self, settings):
        creds_file = settings['CREDS_FILE']
        scopes = settings['SCOPES']
        return service_account.Credentials.from_service_account_file(
            creds_file, scopes=scopes)