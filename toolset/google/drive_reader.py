# -*- encoding: UTF-8 -*-

import ..utils.http_utils as http_utils

class GoogleDriveReader:
    def __init__(driver_service):
        self.service = driver_service

    # publish your doc to web and get from the public url
    # especially useful to get tsv file from spreadsheet
    def get_via_url(url):
        return http_utils.get_content(url)

    def get_file_metadata(self, file_id, mime_type):

    def get(self, file_id, mime_type):
        self.service.files().export(
                fileId=file_id,
                mimeType=mime_type).execute()
