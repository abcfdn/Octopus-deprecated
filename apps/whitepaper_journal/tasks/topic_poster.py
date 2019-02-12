# -*- encoding: UTF-8 -*-

import os

from datetime import datetime
from toolset.image.composer import ImageComposer, ImagePiece
from toolset.google.drive import GoogleDrive
import toolset.utils.util as util
from app.base import Task

IMG_MIME = 'image/jpeg'
logger = logging.getLogger('whitepaper_journal_topic_poster')


class WhitepaperJournalTopicPoster(Task):
    TXT_FIELDS = ['datetime', 'session_name', 'presenter_name',
                  'presenter_title', 'address']
    IMG_FIELDS = ['presenter_avatar']

    def __init__(self, drive_service, common_config, task_config):
        self.drive_service = drive_service
        super().__init__(common_config, task_config)
        self.remote_output = settings['output']
        self.txt_style = settings['txt_style']
        self.img_style = settings['img_style']
        self.init_cache(settings['cache'])
        self.reset()

    def init_cache(self, cache_settings):
        self.local_output = os.path.join(local_path, 'generated')
        util.create_if_not_exist(self.local_output)

        self.template_dir = os.path.join(local_path, 'template')
        util.create_if_not_exist(self.template_dir)
        self.drive_service.sync_folder(cache_settings['template'], self.template_dir)

        self.avatar_dir = os.path.join(local_path, 'avatar')
        util.create_if_not_exist(self.avatar_dir)
        self.drive_service.sync_folder(cache_settings['avatar'], self.avatar_dir)

        self.font_dir = os.path.join(local_path, 'font')
        util.create_if_not_exist(self.font_dir)
        self.drive_service.sync_folder(cache_settings['font'], self.font_dir)

    def reset(self):
        header_file = os.path.join(self.template_dir, 'header.png')
        self.header = ImagePiece.from_file(header_file)

        tail_file = os.path.join(self.template_dir, 'tail.png')
        self.tail = ImagePiece.from_file(tail_file)

        schedule_file = os.path.join(self.template_dir, 'schedule.png')
        self.schedule = ImagePiece.from_file(schedule_file)

        event_sep_file = os.path.join(self.template_dir, 'item_sep.png')
        self.event_sep = ImagePiece.from_file(event_sep_file)

        logo_file = os.path.join(self.template_dir, 'logo.png')
        self.logo = ImagePiece(logo_file)

        self.content = [self.header, self.schedule]

    def draw_text(self, img, text, settings):
        settings['font']['font_dir'] = self.font_dir
        img.draw_text(text, settings)

    # events should belong to same topic
    def add_topic(self, events):
        if not len(events):
            return

        logger.info('Rendering topic {}'.format(event[0]['topic'])
        topic_file = os.path.join(self.template_dir, 'topic.png')
        topic_img = ImagePiece.from_file(topic_file)
        self.draw_text(topic_img,
                       'Topic: ' + events[0]['topic'],
                       self.txt_style['topic'])
        self.content.append(topic_img)

        event_imgs =[self.create_event(event) for event in events]
        event_seps = [self.event_sep] * len(event_imgs)
        self.content.extend([img for pair in zip(event_imgs, event_seps)
                                 for img in pair][:-1])

    def create_event(self, event):
        logger.info('Rendering event {}'.format(event['session_name'])

        event['datetime'] = '{} {}'.format(event['date'], event['time'])
        event['address'] = event['address1'] + '\n' + event['address2']

        item_file = os.path.join(self.template_dir, 'item.png')
        event_img = ImagePiece.from_file(item_file)
        for field in self.TXT_FIELDS:
            self.draw_text(event_img, event[field], self.txt_style[field])

        avatar_file = util.get_file(self.avatar_dir, event['presenter_name'])
        if not avatar_file:
            raise('No avatar file found for {}'.format(event['presenter_name']))
        avatar_img = ImagePiece.from_file(avatar_file)
        avatar_img.to_circle_thumbnail(tuple(self.img_style['avatar']['size']))

        composer = ImageComposer([event_img, avatar_img])
        composer.zstack(self.img_style['avatar']['start'])
        return composer.to_img_piece()

    def process(self):
        self.content.append(self.tail)
        composer = ImageComposer(self.content)
        composer.vstack()

        if not filename:
            filename = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        filepath = os.path.join(self.local_output, filename + '.png')
        composer.save(filepath)
        if upload:
            self.drive_service.upload_file(
                    filepath, IMG_MIME, self.remote_output)


