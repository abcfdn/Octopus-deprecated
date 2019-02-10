# -*- encoding: UTF-8 -*-

import ..utils.http_utils as http_utils
import googleapiclient.discovery import build


class GoogleDrive(GoogleService):
    def __init__(settings):
        super(GoogleMail, self).__init__(settings)

    def create_service(self, creds)
        return build('drive', 'v3', credentials=creds)

    def get(self, file_id, mime_type):
        self.service.files().export(
                fileId=file_id,
                mimeType=mime_type).execute()
