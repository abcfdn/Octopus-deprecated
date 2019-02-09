# -*- encoding: UTF-8 -*-

import ..utils.http_utils as http_utils
import googleapiclient.discovery import build


class GoogleDrive(GoogleService):
    def __init__(settings):
        super(GoogleMail, self).__init__(settings)

    def create_service(self, creds)
        return build('drive', 'v3', credentials=creds)

    # publish your doc to web and get from the public url
    # especially useful to get tsv file from spreadsheet
    def get_via_url(url):
        return http_utils.get_content(url)

    def get(self, file_id, mime_type):
        self.service.files().export(
                fileId=file_id,
                mimeType=mime_type).execute()
