# -*- encoding: UTF-8 -*-

import os
import io

from googleapiclient.discovery import build
from .service import GoogleService
from apiclient.http import MediaIoBaseDownload

DELEGATED_USER = 'contact@abcer.world'


class GoogleDrive(GoogleService):
    def __init__(self, settings):
        super().__init__(settings)

    def create_service(self, creds):
        delegated_creds = creds.with_subject(DELEGATED_USER)
        return build('drive', 'v3', credentials=delegated_creds)

    def download_file(self, file_id, local_filepath):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(local_filepath, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download {}%%.".format(int(status.progress() * 100)))

    def sync_folder(self, folder_id, local_path, overwrite=False):
        existing = set()
        if not overwrite:
            existing = set(os.listdir(local_path))

        query = "'{}' in parents".format(folder_id)
        response = self.service.files().list(
            q=query, spaces='drive', fields='files(id, name)').execute()
        for f in response.get('files', []):
            file_name = f.get('name')
            if file_name not in existing:
                dest = os.path.join(local_path, file_name)
                print('Downloading {} to {}'.format(file_name, dest))
                self.download_file(f.get('id'), dest)
