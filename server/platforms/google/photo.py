# -*- encoding: UTF-8 -*-

import logging

from googleapiclient.discovery import build
from .service import GoogleService
import jwt

logger = logging.getLogger('google_photo')

class GooglePhoto(GoogleService):
    UPLOAD_URL = 'https://photoslibrary.googleapis.com/v1/uploads'

    def __init__(self, google_creds):
        super().__init__(google_creds)

    def create_service(self, creds):
        return build('photoslibrary',
                     'v1',
                     credentials=creds,
                     cache_discovery=False)

    def upload(self, filepath):
        logger.info('Uploading {} to google server...'.format(filepath))
        f = open(filepath, 'rb').read();
        headers = {
            'Authorization': "Bearer " + self.service.credentials.access_token,
            'Content-Type': 'application/octet-stream',
            'X-Goog-Upload-File-Name': filepath,
            'X-Goog-Upload-Protocol': "raw",
        }
        r = requests.post(self.UPLOAD_URL, data=f, headers=headers)
        logger.info('Upload token {}'.format(r.content))
        return r.content

    def create_item(self, album_id, filepath, file_description):
        upload_token = self.upload(filepath)
        body = {
            "albumId": album_id,
            "newMediaItems": [{
                "description": file_description,
                "simpleMediaItem": {
                    "uploadToken": upload_token
                }
            }]
        }
        results = self.service.mediaItems().batchCreate(body=body).execute()
        print(results)

    def get_photo(self, photo_id):
        searchBody = {"mediaItemId": photo_id}
        results = self.service.mediaItems().get(body=searchBody).execute()

    def get_photos(self, album_id, max_cnt=100):
        searchBody = {
            "albumId": album_id,
            "pageSize": 10
        }
        results = self.service.mediaItems().search(body=searchBody).execute()
        items = results.get('mediaItems', [])
        while 'nextPageToken' in results and len(items) < max_cnt:
            searchBody['pageToken'] = results['nextPageToken']
            results = self.service.mediaItems().search(body=searchBody).execute()
            items.extend(results['mediaItems'])
        return items

    def list_albums(self):
        return self.service.sharedAlbums().list().execute()
