# -*- encoding: UTF-8 -*-

from google.oauth2 import service_account


class GoogleService:
    DELEGATED_USER = 'contact@abcer.world'

    def __init__(self, settings):
        creds = self.load_creds(settings)
        delegated_creds = creds.with_subject(self.DELEGATED_USER)
        self.service = self.create_service(delegated_creds)

    def create_service(self, creds):
        raise("Not Implemented")

    def load_creds(self, settings):
        creds_file = settings['creds_file']
        scopes = settings['scopes']
        return service_account.Credentials.from_service_account_file(
            creds_file, scopes=scopes)
