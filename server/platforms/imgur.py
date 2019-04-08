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

    def upload(self, photo_id, photo_path):
        config = {
            'name':  photo_id,
            'title': photo_id,
            'description': photo_id}
        image = self.client.upload_from_path(photo_path, config=config, anon=False)
        logger.info(image)
        return image['id']

    def upload_photos(self, photos, album_id):
        ids = []
        for photo_id in photos.keys():
            ids.append(self.upload(photo_id, photos[photo_id]))
        logger.info(ids)
        self.client.album_add_images(album_id, ids)

    def get_photos(self, album_id, max_cnt=1000):
        return self.client.get_album_images(album_id)
