# -*- encoding: UTF-8 -*-

import os
import logging

from datetime import datetime
from toolset.image.composer import ImageComposer, ImagePiece
from toolset.google.sheet import GoogleSheet
import toolset.utils.util as util

from apps.base import Task
from .poster_base import WhitepaperJournalPosterBase

logger = logging.getLogger('whitepaper_journal_event_poster')


class WhitepaperJournalEventPoster(WhitepaperJournalPosterBase):
    FIELDS_TO_COMPARE = ['session_name', 'presenter_name']

    def __init__(self, common_config):
        super().__init__(common_config)
        self.txt_style = self.config['txt_style']
        self.img_style = self.config['img_style']

    @classmethod
    def add_parser(cls, parser):
        topic_poster_parser = parser.add_parser(
            cls.__name__, help='create whitepaper journal event poster')
        group = topic_poster_parser.add_mutually_exclusive_group()
        group.add_argument('--event',
                           help='event_id, which is presenter name + date')

    def reset(self):
        self.header = self.get_common_template('header.png')
        self.keywords = self.get_common_template('meetup_keywords.png')
        self.meetup = self.get_common_template('meetup.png')
        self.tail = self.get_common_template('tail.png')

        self.datetime = self.get_template('datetime.png')
        self.location = self.get_template('location.png')
        self.imgs = [self.header, self.keywords, self.meetup]

    def get_event_id(self, event):
        return '{},{}'.format(event['site'], event['date'])

    def get_schedule(self, event_id):
        for schedule in self.schedules:
            if event_id.lower() == self.get_event_id(schedule).lower():
                return schedule
        return None

    def get_event(self, event_id):
        schedule = self.get_schedule(event_id)
        if not schedule:
            logger.warning('No schedule found')
            return None

        for event in self.events:
            matched = True
            for f in self.FIELDS_TO_COMPARE:
                matched &= (
                    event[f].strip().lower() == schedule[f].strip().lower())
            if matched:
                event['schedule'] = schedule
                return event
        return None

    def draw_datetime(self, event):
        date_time = [self.readable_datetime(event['schedule']['date']),
                     event['schedule']['time']]
        self.draw_text(self.datetime, date_time, self.txt_style['datetime'])
        self.imgs.append(self.datetime)

    def draw_address(self, event):
        address = [event['schedule']['address1'], event['schedule']['address2']]
        self.draw_text(self.location, address, self.txt_style['address'])
        self.imgs.append(self.location)

    def draw_speaker(self, event):
        title = self.get_template('title.png')
        self.draw_text(title, ['Presenter'], self.txt_style['title'])

        content = self.get_template('content.png')
        avatar = self.get_avatar(event)
        composer = ImageComposer([content, avatar])
        composer.zstack(self.img_style['avatar']['box'],
                        self.img_style['avatar']['align'])
        self.draw_text(content,
                       [event['presenter_name']],
                       self.txt_style['presenter_name'])
        self.draw_text(content,
                       [event['title'], event['company/organization']],
                       self.txt_style['presenter_title'])

        self.draw_text(content,
                       [event['self-introduction']],
                       self.txt_style['presenter_introduction'])

        self.imgs.extend([title, content])

    def draw_project(self, event):
        title = self.get_template('title.png')
        self.draw_text(
            title, ['Project'], self.txt_style['title'])

        content = self.get_template('content.png')
        logo = self.get_logo(event)
        composer = ImageComposer([content, logo])
        composer.zstack(self.img_style['logo']['box'],
                        self.img_style['logo']['align'])

        self.draw_text(content,
                       [event['short_description']],
                       self.txt_style['project_description'])
        self.imgs.extend([title, content])

    def draw_session(self, event):
        content = self.get_template('content.png')
        self.draw_text(content,
                       [event['session_name']],
                       self.txt_style['session_name'])
        self.draw_text(content,
                       [event['summary']],
                       self.txt_style['session_summary'])
        self.imgs.append(content)

    def draw(self, event):
        self.reset()
        self.draw_session(event)
        self.draw_datetime(event)
        self.draw_address(event)
        self.draw_speaker(event)
        self.draw_project(event)
#        self.imgs.append(self.tail)

    def process(self, args):
        event = self.get_event(args.event)
        self.draw(event)
        composer = ImageComposer(self.imgs)
        composer.vstack()
        self.save(composer, filename='event', upload=False)

