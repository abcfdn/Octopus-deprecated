# -*- encoding: UTF-8 -*-

import json
import logging
from imgurpython import ImgurClient

logger = logging.getLogger('imgur')
logger.setLevel(logging.INFO)

class Imgur:
    def __init__(self, creds_file):
        with open(creds_file, 'r') as f:
            creds = json.load(f)
        self.client = ImgurClient(
            creds['client_id'], creds['client_secret'])

    def upload_photo(self, photo_id, photo_path):
        config = {
            'name':  'N/A',
            'title': 'N/A',
            'description': 'N/A'}
        image = self.client.upload_from_path(photo_path, config=config, anon=False)
        logger.info('Uploaded photo {} for {}'.format(image, photo_id))
        image['local_path'] = photo_path
        return image

    def upload_photos(self, photos):
        return {
            photo_id: self.upload(photo_id, photos[photo_id])
            for photo_id in photos.keys()
        }

    def get_photos(self, album_id, max_cnt=1000):
        return self.client.get_album_images(album_id)
