# -*- encoding: UTF-8 -*-

import os
import logging

from datetime import datetime
from toolset.image.composer import ImageComposer, ImagePiece
from toolset.google.sheet import GoogleSheet
import toolset.utils.util as util
from apps.base import Task

IMG_MIME = 'image/jpeg'
logger = logging.getLogger('whitepaper_journal_topic_poster')


class WhitepaperJournalPoster(Task):
    TXT_FIELDS = ['datetime', 'session_name', 'presenter_name',
                  'presenter_title', 'address']
    IMG_FIELDS = ['presenter_avatar']

    def __init__(self, common_config):
        super().__init__(common_config)
        self.events = self.load_events()

        self.txt_style = self.config['txt_style']
        self.img_style = self.config['img_style']

        self.output_dir = self.config['data']['output']
        self.font_dir = self.config['data']['font']['local']
        self.avatar_dir = self.config['data']['avatar']['local']
        self.template_dir = self.config['data']['template']['local']

    def load_events(self):
        sheet_service = GoogleSheet(self.config['google'])
        events = sheet_service.read_as_map(
            self.config['data']['schedule']['remote'], (2, 200))
        events.sort(key=lambda k: k['date'])
        return events

    def get_template_img(self, basename):
        filename = os.path.join(self.template_dir, basename)
        return ImagePiece.from_file(filename)

    def get_avatar(self, name):
        avatar_file = util.get_file(self.avatar_dir, name)
        if not avatar_file:
            raise('Missing avatar file for {}'.format(name))
        avatar_img = ImagePiece.from_file(avatar_file)
        avatar_img.to_circle_thumbnail(tuple(self.img_style['avatar']['size']))
        return avatar_img

    def reset(self):
        self.header = self.get_template_img('header.png')
        self.tail = self.get_template_img('tail.png')
        self.schedule = self.get_template_img('schedule.png')
        self.event_sep = self.get_template_img('item_sep.png')
        self.logo = self.get_template_img('logo.png')
        self.content = [self.header, self.schedule]

    def draw_text(self, img, text, settings):
        font_settings = settings['font']
        font = img.get_font(self.font_dir, settings['font'])
        img.draw_text(text, font, settings)

    # events should belong to same topic
    def add_topic(self, topic):
        filtered = [event for event in self.events if event['topic'] == topic]
        if not len(filtered):
            logging.warning('No event found for topic {}'.format(topic))
            return

        logger.info('Rendering topic {}'.format(topic))
        topic_img = self.get_template_img('topic.png')
        self.draw_text(topic_img,
                       'Topic: {}'.format(topic),
                       self.txt_style['topic'])
        self.content.append(topic_img)

        event_imgs =[self.create_event(event) for event in filtered]
        event_seps = [self.event_sep] * len(event_imgs)
        self.content.extend([img for pair in zip(event_imgs, event_seps)
                                 for img in pair][:-1])

    def create_event(self, event):
        logger.info('Rendering event {}'.format(event['session_name']))

        event['datetime'] = '{} {}'.format(event['date'], event['time'])
        event['address'] = event['address1'] + '\n' + event['address2']

        event_img = self.get_template_img('item.png')
        for field in self.TXT_FIELDS:
            self.draw_text(event_img, event[field], self.txt_style[field])

        avatar_img = self.get_avatar(event['presenter_name'])
        composer = ImageComposer([event_img, avatar_img])
        composer.zstack(self.img_style['avatar']['start'])
        return composer.to_img_piece()

    def save(self, composer, filename=None, upload=True):
        if not filename:
            filename = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        filepath = os.path.join(self.output_dir['local'], filename + '.png')
        composer.save(filepath)
        if upload:
            self.drive_service.upload_file(
                    filepath, IMG_MIME, self.output_dir['remote'])

    def process(self, args):
        self.reset()
        for topic in args.topics.split(','):
            self.add_topic(topic)
        self.content.append(self.tail)
        composer = ImageComposer(self.content)
        composer.vstack()
        self.save(composer)

