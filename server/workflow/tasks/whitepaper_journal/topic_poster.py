# -*- encoding: UTF-8 -*-

import os
import logging

from server.platforms.image.composer import ImageComposer, ImagePiece
from server.platforms.google.sheet import GoogleSheet
import server.platforms.utils.util as util

from apps.base import Task
from .poster_base import WhitepaperJournalPosterBase

logger = logging.getLogger('whitepaper_journal_topic_poster')


class WhitepaperJournalTopicPoster(WhitepaperJournalPosterBase):
    TXT_FIELDS = ['datetime', 'session_name', 'presenter_name',
                  'presenter_title']

    def __init__(self, common_config):
        super().__init__(common_config)

    @classmethod
    def add_parser(cls, parser):
        topic_poster_parser = parser.add_parser(
            cls.__name__, help='create whitepaper journal topic poster')
        group = topic_poster_parser.add_mutually_exclusive_group()
        group.add_argument('--topics', help='create topic poster, comma separated')

    def reset(self):
        self.header = self.get_common_template('header.png')
        self.keywords = self.get_common_template('abc_keywords.png')
        self.meetup = self.get_common_template('meetup.png')
        self.tail = self.get_common_template('tail.png')

        self.schedule_img = self.get_template('schedule.png')
        self.schedule_sep = self.get_template('item_sep.png')
        self.content = [self.header,
                        self.keywords,
                        self.meetup,
                        self.schedule_img]

    def add_topic(self, topic):
        filtered = [schedule for schedule in self.schedules
            if schedule['topic'].strip().lower() == topic.strip().lower()]
        if not len(filtered):
            logging.warning('No schedule found for topic {}'.format(topic))
            return

        logger.info('Rendering topic {}'.format(topic))
        topic_img = self.get_template('topic.png')
        self.draw_text(topic_img,
                       ['Topic: {}'.format(topic)],
                       self.txt_style['topic'])
        self.content.append(topic_img)

        schedule_imgs =[self.create_schedule(schedule) for schedule in filtered]
        schedule_seps = [self.schedule_sep] * len(schedule_imgs)
        self.content.extend([img for pair in zip(schedule_imgs, schedule_seps)
                                 for img in pair][:-1])

    def create_schedule(self, schedule):
        logger.info('Rendering schedule {}'.format(schedule['session_name']))
        schedule_img = self.get_template('item.png')

        self.draw_text(
            schedule_img,
            [schedule['address1'], schedule['address2']],
            self.txt_style['address'])

        event_time = self.readable_time({'schedule': schedule})
        schedule['datetime'] = '{} {}'.format(schedule['date'], event_time)
        for field in self.TXT_FIELDS:
            self.draw_text(schedule_img, [schedule[field]], self.txt_style[field])

        avatar_img = self.get_avatar(schedule)
        composer = ImageComposer([schedule_img, avatar_img])
        composer.zstack(self.img_style['avatar']['box'],
                        self.img_style['avatar']['align'])
        return composer.to_img_piece()

    def process(self, args):
        self.reset()
        for topic in args.topics.split(','):
            self.add_topic(topic)
        self.content.append(self.tail)
        composer = ImageComposer(self.content)
        composer.vstack()
        self.save(composer, filename='topic', upload=False)

