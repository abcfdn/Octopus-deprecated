# -*- encoding: UTF-8 -*-

import os
import logging

import calendar
from datetime import datetime, timedelta
import pytz

from server.platforms.image.composer import ImageComposer, ImagePiece
from server.platforms.google.sheet import GoogleSheet
import server.platforms.utils.util as util
from server.platforms.image.qrcode import create_qr_code

from server.workflow.base import Task
from .poster_base import WhitepaperJournalPosterBase
from pprint import pprint

logger = logging.getLogger('whitepaper_journal_session_poster')


class WhitepaperJournalEventPoster(WhitepaperJournalPosterBase):
    def __init__(self, google_creds):
        super().__init__(google_creds)
        self.txt_style = self.config['txt_style']
        self.img_style = self.config['img_style']

    def reset(self):
        self.header = self.get_common_template('header.png')
        self.keywords = self.get_common_template('meetup_keywords.png')
        self.meetup = self.get_common_template('meetup.png')
        self.tail = self.get_common_template('tail.png')

        self.datetime = self.get_template('datetime.png')
        self.location = self.get_template('location.png')
        self.imgs = [self.header, self.keywords, self.meetup]

    def readable_datetime(self, schedule):
        start_time = datetime.fromtimestamp(schedule['start_at'])
        weekday = calendar.day_name[start_time.weekday()]
        readable_date = '{}, {}'.format(weekday, start_time.strftime("%B %d, %Y"))

        end_time = start_time + timedelta(0, schedule['duration_as_mins'] * 60)
        readable_time = '{}-{}'.format(start_time.strftime('%I:%M'),
                              end_time.strftime('%I:%M %p'))
        return [readable_date, readable_time]

    def draw_schedule(self, schedule):
        self.draw_text(self.datetime,
                       self.readable_datetime(schedule),
                       self.txt_style['datetime'])
        self.imgs.append(self.datetime)

        if 'address' in schedule and 'location' in schedule:
            address = [schedule['address'], schedule['location']]
            self.draw_text(self.location, address, self.txt_style['address'])
            self.imgs.append(self.location)

        if 'zoom_link' in schedule:
            content = self.get_template('content.png')
            qrcode = ImagePiece(create_qr_code(schedule['zoom_link']))
            qrcode.resize((150, 150))
            composer = ImageComposer([content, qrcode])
            composer.zstack(self.img_style['qrcode']['box'],
                            self.img_style['qrcode']['align'])
            decription = ["Scan the QR Code to join us from zoom"]
            decription.append("Passcode: {}".format(schedule["zoom_passcode"]))
            self.draw_text(content, decription, self.txt_style['online_link'])
            content.crop_bottom(250)
            self.imgs.append(content)

    def draw_speaker(self, presenter):
        title = self.get_template('title.png')
        self.draw_text(title, ['Presenter'], self.txt_style['title'])

        content = self.get_template('content.png')
        avatar = self.get_avatar(presenter)
        composer = ImageComposer([content, avatar])
        composer.zstack(self.img_style['avatar']['box'],
                        self.img_style['avatar']['align'])
        self.draw_text(content,
                       [presenter['full_name']],
                       self.txt_style['presenter_name'])
        self.draw_text(content,
                       [presenter['title'], presenter['orgnization']],
                       self.txt_style['presenter_title'])

        y_pos = self.draw_text(
            content,
            [presenter['self_intro']],
            self.txt_style['presenter_introduction'])
        content.crop_bottom(y_pos + 20)
        self.imgs.extend([title, content])

    def draw_project(self, project):
        title = self.get_template('title.png')
        self.draw_text(
            title, ['Project'], self.txt_style['title'])

        content = self.get_template('content.png')
        logo = self.get_logo(project)
        composer = ImageComposer([content, logo])
        composer.zstack(self.img_style['logo']['box'],
                        self.img_style['logo']['align'])

        y_pos = self.draw_text(
            content,
            [project.get('long_description', '') or
                project.get('short_description', '')],
            self.txt_style['project_description'])
        content.crop_bottom(y_pos + 20)
        self.imgs.extend([title, content])

    def draw_session(self, session):
        title = self.get_template('title.png')
        self.draw_text(
            title, ['Summary'], self.txt_style['title'])

        content = self.get_template('content.png')
        y_pos = self.draw_text(
            content,
            [session.get('highlight', '') or session['summary']],
            self.txt_style['session_summary'])
        content.crop_bottom(y_pos + 20)
        self.imgs.extend([title, content])

    def draw_session_name(self, session):
        content = self.get_template('content.png')
        y_pos = self.draw_text(
            content,
            [session['name']],
            self.txt_style['session_name'])
        content.crop_bottom(y_pos + 20)
        self.imgs.extend([content])

    def draw(self, session, presenter):
        self.reset()
        self.draw_session_name(session)
        self.draw_schedule(session['schedule'])
        self.draw_speaker(presenter)
        self.draw_project(presenter['project'])
        self.draw_session(session)
        self.imgs.append(self.tail)

    def process(self, session_id):
        session = self.get_session(session_id)
        presenter = self.get_presenter(session['presenter'])
        self.draw(session, presenter)
        composer = ImageComposer(self.imgs)
        composer.vstack()
        self.save(composer, filename=str(session_id), upload=False)
