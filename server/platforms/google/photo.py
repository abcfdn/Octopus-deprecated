# -*- encoding: UTF-8 -*-

import logging

import requests

from googleapiclient.discovery import build
from .service import GoogleService
import jwt

logger = logging.getLogger('google_photo')

class GooglePhoto(GoogleService):
    UPLOAD_URL = 'https://photoslibrary.googleapis.com/v1/uploads'
    MEDIA_ITEM_URL = 'https://photoslibrary.googleapis.com/v1/mediaItems'

    def __init__(self, google_creds):
        super().__init__(google_creds)
        self.credentials = google_creds

    def create_service(self, creds):
        return build('photoslibrary',
                     'v1',
                     credentials=creds,
                     cache_discovery=False)

    def upload(self, filepaths):
        return {self.upload_one(f) : f for f in filepaths}

    def upload_one(self, filepath):
        logger.info('Uploading {} to google server...'.format(filepath))
        print('Uploading {}...'.format(filepath))
        f = open(filepath, 'rb').read();
        headers = {
            'Authorization': "Bearer " + self.credentials.token,
            'Content-Type': 'application/octet-stream',
            'X-Goog-Upload-File-Name': filepath,
            'X-Goog-Upload-Protocol': "raw",
        }
        r = requests.post(self.UPLOAD_URL, data=f, headers=headers)
        return r.content.decode('utf-8')

    def batch_create_items(self, tokens):
        print('Creating {} items in total'.format(len(tokens)))
        num_batch = int(len(tokens) / 49 + 1)
        results = []
        for i in range(0, num_batch):
            print('Creating batch {}...'.format(i))
            token_to_process = tokens[49*i: 49*i + 48]
            new_items = self.create_items(token_to_process).get('newMediaItemResults', [])
            results.extend(new_items)
        return results

    def create_items(self, tokens):
        if not tokens:
            return []
        body = {"newMediaItems": []}
        for token in tokens:
            body["newMediaItems"].append({
                "simpleMediaItem": {
                    "uploadToken": token
                }
            })
        return self.service.mediaItems().batchCreate(body=body).execute()

    def get_photo(self, photo_id):
        headers = {
            'Authorization': "Bearer " + self.credentials.token,
            'Content-Type': 'application/json',
        }
        r = requests.get('{}/{}'.format(self.MEDIA_ITEM_URL, photo_id), headers=headers)
        return r.content.decode('utf-8')

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
