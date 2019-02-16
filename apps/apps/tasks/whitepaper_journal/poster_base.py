# -*- encoding: UTF-8 -*-

import os
import logging

from datetime import datetime

from toolset.image.composer import ImageComposer, ImagePiece
import toolset.utils.util as util
from .base import WhitepaperJournalBase


IMG_MIME = 'image/jpeg'


class WhitepaperJournalPosterBase(WhitepaperJournalBase):
    NUM_OF_ROWS_TO_READ = 1000

    def __init__(self, common_config):
        super().__init__(common_config)
        self.txt_style = self.config['txt_style']
        self.img_style = self.config['img_style']

    def get_common_template(self, basename):
        template_dir = self.config['data']['common_template']['local']
        return ImagePiece.from_file(os.path.join(template_dir, basename))

    def get_template(self, basename):
        template_dir = self.config['data']['template']['local']
        return ImagePiece.from_file(os.path.join(template_dir, basename))

    def get_logo_by_project(self, project_name):
        logo_file = util.get_file(self.config['data']['logo']['local'],
                                  project_name)
        if not logo_file:
            return None
        logo_img = ImagePiece.from_file(logo_file)
        logo_img.to_thumbnail(tuple(self.img_style['logo']['size']))
        return logo_img

    def get_logo(self, event):
        project_name = event['project_name'].strip()
        logo_img = self.get_logo_by_project(project_name)
        if logo_img:
            return logo_img

        logo_dir = self.config['data']['logo']['local']
        origin_path = self.drive_service.download_from_url(
            event['project_logo'], logo_dir)
        ext = os.path.splitext(origin_path)[1]
        newpath = os.path.join(logo_dir, project_name + ext)
        os.rename(origin_path, newpath)
        return self.get_logo_by_project(project_name)

    def get_avatar_by_name(self, name):
        avatar_file = util.get_file(self.config['data']['avatar']['local'],
                                    name)
        if not avatar_file:
            return None
        avatar_img = ImagePiece.from_file(avatar_file)
        avatar_img.to_circle_thumbnail(tuple(self.img_style['avatar']['size']))
        return avatar_img

    def get_avatar(self, event):
        name = event['presenter_name'].strip()
        avatar_img = self.get_avatar_by_name(name)
        if avatar_img:
            return avatar_img

        avatar_dir = self.config['data']['avatar']['local']
        origin_path = self.drive_service.download_from_url(
            event['photo'], avatar_dir)
        ext = os.path.splitext(origin_path)[1]
        newpath = os.path.join(avatar_dir, name + ext)
        os.rename(origin_path, newpath)
        return self.get_avatar_by_name(name)

    def draw_text(self, img, lines, settings):
        font = img.get_font(self.config['data']['font']['local'],
                            settings['font'])
        img.draw_text(lines, font, settings)

    def save(self, composer, filename=None, upload=True):
        if not filename:
            filename = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

        output_dir = self.config['data']['output']
        filepath = os.path.join(output_dir['local'], filename + '.png')
        composer.save(filepath)
        if upload:
            self.drive_service.upload_file(
                    filepath, IMG_MIME, output_dir['remote'])

    def reset(self):
        raise('Not Implemented')

    def process(self, args):
        raise('Not Implemented')

