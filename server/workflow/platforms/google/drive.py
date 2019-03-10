# -*- encoding: UTF-8 -*-

import os
import io
import logging

from urllib.parse import urlparse, parse_qs

from googleapiclient.discovery import build
from .service import GoogleService
from apiclient.http import MediaIoBaseDownload, MediaFileUpload

logger = logging.getLogger('google_drive')


class GoogleDrive(GoogleService):
    def __init__(self, settings):
        super().__init__(settings)

    def create_service(self, creds):
        return build('drive',
                     'v3',
                     credentials=creds,
                     cache_discovery=False)

    def upload_file(self, localpath, mimetype, parent):
        logger.info('Uploading {} to drive {}'.format(localpath, parent))
        filename = os.path.basename(localpath)
        file_metadata = {'name': filename, 'parents': [parent]}
        media = MediaFileUpload(localpath, mimetype=mimetype)
        f = self.service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
        logger.info('Uploaded with file_id={}'.format(f.get('id')))

    def get_file_id_from_url(self, url):
        query = parse_qs(urlparse(url).query)
        ids = query.get('id', [])
        if not len(ids):
            logger.warning('No file to download')
            return None
        return ids[0]

    def download_from_url(self, url, localdir):
        file_id = self.get_file_id_from_url(url)
        file_metadata = self.service.files().get(
                fileId=file_id, fields="name").execute()
        localpath = os.path.join(localdir, file_metadata['name'])
        self.download_file(file_id, localpath)
        return localpath

    def download_file(self, file_id, localpath, overwrite=False):
        if os.path.exists(localpath) and not overwrite:
            logger.info('File {} exists, skipping'.format(localpath))
            return

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
        query = "'{}' in parents".format(folder_id)
        response = self.service.files().list(
            q=query, spaces='drive', fields='files(id, name)').execute()
        for f in response.get('files', []):
            dest = os.path.join(localpath, f.get('name'))
            self.download_file(f.get('id'), dest)
