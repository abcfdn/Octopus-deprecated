# -*- encoding: UTF-8 -*-

import os
import logging

from datetime import datetime
from toolset.image.composer import ImageComposer, ImagePiece
from toolset.google.sheet import GoogleSheet
import toolset.utils.util as util
from apps.base import Task

logger = logging.getLogger('whitepaper_journal_topic_poster')


class WhitepaperJournalTopicPoster(Task):
    TXT_FIELDS = ['datetime', 'session_name', 'presenter_name',
                  'presenter_title', 'address']
    IMG_FIELDS = ['presenter_avatar']

    def __init__(self, common_config):
        super().__init__(common_config)
        self.txt_style = self.config['txt_style']
        self.img_style = self.config['img_style']

    def reset(self):
        self.header = self.get_common_template('header.png')
        self.keywords = self.get_common_template('abc_keywords.png')
        self.meetup = self.get_common_template('meetup.png')
        self.tail = self.get_common_template('tail.png')

        self.schedule = self.get_template('schedule.png')
        self.event_sep = self.get_template('item_sep.png')
        self.content = [self.header, self.keywords, self.meetup, self.schedule]

    def add_topic(self, topic):
        filtered = [event for event in self.events if event['topic'] == topic]
        if not len(filtered):
            logging.warning('No event found for topic {}'.format(topic))
            return

        logger.info('Rendering topic {}'.format(topic))
        topic_img = self.get_template('topic.png')
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

        event_img = self.get_template('item.png')
        for field in self.TXT_FIELDS:
            self.draw_text(event_img, event[field], self.txt_style[field])

        avatar_img = self.get_avatar(event['presenter_name'])
        composer = ImageComposer([event_img, avatar_img])
        composer.zstack(self.img_style['avatar']['start'])
        return composer.to_img_piece()

    def process(self, args):
        self.reset()
        for topic in args.topics.split(','):
            self.add_topic(topic)
        self.content.append(self.tail)
        composer = ImageComposer(self.content)
        composer.vstack()
        self.save(composer)

