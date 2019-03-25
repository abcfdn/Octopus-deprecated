# -*- encoding: UTF-8 -*-

import os
import logging
from datetime import datetime, timedelta

import server.platforms.utils.util as util
from server.platforms.image.composer import ImagePiece

from server.workflow.base import Task
from server.workflow.constants import MEMBERSHIP_APP

logger = logging.getLogger('membership_card')


class MembershipCard(Task):
    def __init__(self, google_creds):
        super().__init__(google_creds)
        self.txt_style = self.config['txt_style']
        self.template_dir = self.config['data']['template']['local']

    def app_name(self):
        return MEMBERSHIP_APP

    def draw_text(self, img, lines, settings):
        font = img.get_font(self.config['data']['font']['local'],
                            settings['font'])
        return img.draw_text(lines, font, settings)

    def readable_date(self, started_at):
        start_time = datetime.fromtimestamp(started_at)
        # UTC to PST
        start_time = start_time - timedelta(seconds=8*3600)
        return start_time.strftime("%Y/%m")

    def process(self, member):
        output_dir = self.config['data']['output']
        filepath = os.path.join(output_dir['local'], member['email'] + '.png')
        exists = os.path.isfile('/path/to/file')
        if not exists:
            content = ImagePiece.from_file(
                os.path.join(self.template_dir, 'membership_card.png'))
            self.draw_text(
                content,
                [member['name']],
                self.txt_style['name'])
            self.draw_text(
                content,
                [self.readable_date(member['started_at'])],
                self.txt_style['date'])
            content.save(filepath)
        return filepath
