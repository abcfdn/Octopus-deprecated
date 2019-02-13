# -*- encoding: UTF-8 -*-

import os
import io
import logging

from googleapiclient.discovery import build
from .service import GoogleService
from apiclient.http import MediaIoBaseDownload, MediaFileUpload

DELEGATED_USER = 'contact@abcer.world'
logger = logging.getLogger('google_drive')


class GoogleDrive(GoogleService):
    def __init__(self, settings):
        super().__init__(settings)

    def create_service(self, creds):
        delegated_creds = creds.with_subject(DELEGATED_USER)
        return build('drive', 'v3', credentials=delegated_creds)

    def upload_file(self, localpath, mimetype, parent):
        logger.info('Uploading {} to drive {}'.format(localpath, parent))
        filename = os.path.basename(localpath)
        file_metadata = {'name': filename, 'parents': [parent]}
        media = MediaFileUpload(localpath, mimetype=mimetype)
        f = self.service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
        logger.info('Uploaded with file_id={}'.format(f.get('id')))

    def download_file(self, file_id, localpath):
        logger.info('Downloading {} from drive to {}'.format(
            file_id, localpath))
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(localpath, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            logging.info("{}%%. downloaded".format(int(status.progress() * 100)))

    def sync_folder(self, folder_id, localpath, overwrite=False):
        logging.info('Syncing folder {} from drive to {}'.format(
            folder_id, localpath))
        existing = set()
        if not overwrite:
            existing = set(os.listdir(localpath))
        else:
            logging.info('overwrite flag is set, will redownload' +
                         'everything and overwrite local files')

        query = "'{}' in parents".format(folder_id)
        response = self.service.files().list(
            q=query, spaces='drive', fields='files(id, name)').execute()
        for f in response.get('files', []):
            file_name = f.get('name')
            if file_name not in existing:
                dest = os.path.join(localpath, file_name)
                self.download_file(f.get('id'), dest)
