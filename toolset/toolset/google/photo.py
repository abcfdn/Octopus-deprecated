# -*- encoding: UTF-8 -*-

import logging

from googleapiclient.discovery import build
from .service import GoogleService

logger = logging.getLogger('google_photo')

class GooglePhoto(GoogleService):
    def __init__(self, settings):
        super().__init__(settings)

    def create_service(self, creds):
        return build('photoslibrary',
                     'v1',
                     credentials=creds,
                     cache_discovery=False)

    def get_photos(self, album_id):
        searchbody = {"albumId": album_id, "pageSize": 50}
        results = self.service.mediaItems().search(body=searchbody).execute()
#        results = self.service.sharedAlbums().list().execute()
        print(results)
