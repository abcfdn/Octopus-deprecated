# -*- encoding: UTF-8 -*-

import os
import logging

from toolset.image.composer import ImagePiece
from toolset.google.photo import GooglePhoto

from apps.base import Task
from .base import MembershipBase

logger = logging.getLogger('membership_card')


class MembershipCard(MembershipBase):
    def __init__(self, common_config):
        super().__init__(common_config)
        template_dir = self.config['data']['template']['local']
        self.content = ImagePiece.from_file(
            os.path.join(template_dir, 'membership_card.png'))
        self.photo_service = GooglePhoto(self.config['google'])

    @classmethod
    def add_parser(cls, parser):
        event_poster_parser = parser.add_parser(
            cls.__name__, help='create membership card')

    def process(self, args):
        self.photo_service.get_photos(self.config['data']['output']['album_id'])
