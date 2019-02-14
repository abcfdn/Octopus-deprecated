# -*- encoding: UTF-8 -*-

import os
import logging

from datetime import datetime
from toolset.image.composer import ImageComposer, ImagePiece
from toolset.google.sheet import GoogleSheet
import toolset.utils.util as util
from apps.base import Task

IMG_MIME = 'image/jpeg'


class WhitepaperJournalPosterBase(Task):
    def __init__(self, common_config):
        super().__init__(common_config)
        self.events = self.load_events()

    def load_events(self):
        sheet_service = GoogleSheet(self.config['google'])
        events = sheet_service.read_as_map(
            self.config['data']['schedule']['remote'], (2, 200))
        events.sort(key=lambda k: k['date'])
        return events

    def app_name(self):
        return 'whitepaper_journal'

    def get_common_template(self, filename)
        template_dir = self.config['data']['common_template']['local']
        return ImagePiece.from_file(os.path.join(template_dir, basename))

    def get_template(self, basename):
        template_dir = self.config['data']['template']['local']
        return ImagePiece.from_file(os.path.join(template_dir, basename))

    def get_avatar(self, name):
        avatar_file = util.get_file(self.config['data']['avatar']['local'],
                                    name)
        if not avatar_file:
            raise('Missing avatar file for {}'.format(name))
        avatar_img = ImagePiece.from_file(avatar_file)
        avatar_img.to_circle_thumbnail(tuple(self.img_style['avatar']['size']))
        return avatar_img

    def draw_text(self, img, text, settings):
        font_settings = settings['font']
        font = img.get_font(self.config['data']['font']['local'],
                            settings['font'])
        img.draw_text(text, font, settings)

    def save(self, composer, filename=None, upload=True):
        if not filename:
            filename = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

        output_dir = self.config['data']['output']
        filepath = os.path.join(self.output_dir['local'], filename + '.png')
        composer.save(filepath)
        if upload:
            self.drive_service.upload_file(
                    filepath, IMG_MIME, self.output_dir['remote'])

    def reset(self):
        raise('Not Implemented')

    def process(self, args):
        raise('Not Implemented')

