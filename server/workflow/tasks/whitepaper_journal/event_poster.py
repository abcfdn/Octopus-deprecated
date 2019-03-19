# -*- encoding: UTF-8 -*-

import os
import logging

from server.platforms.image.composer import ImageComposer, ImagePiece
from server.platforms.google.sheet import GoogleSheet
import server.platforms.utils.util as util

from server.workflow.base import Task
from .poster_base import WhitepaperJournalPosterBase

logger = logging.getLogger('whitepaper_journal_session_poster')


class WhitepaperJournalEventPoster(WhitepaperJournalPosterBase):
    def __init__(self):
        super().__init__()
        self.txt_style = self.config['txt_style']
        self.img_style = self.config['img_style']

    @classmethod
    def add_parser(cls, parser):
        session_poster_parser = parser.add_parser(
            cls.__name__, help='create whitepaper journal session poster')
        group = session_poster_parser.add_mutually_exclusive_group()
        group.add_argument('--session',
                           help='session_id, which is presenter name + date')

    def reset(self):
        self.header = self.get_common_template('header.png')
        self.keywords = self.get_common_template('meetup_keywords.png')
        self.meetup = self.get_common_template('meetup.png')
        self.tail = self.get_common_template('tail.png')

        self.datetime = self.get_template('datetime.png')
        self.location = self.get_template('location.png')
        self.imgs = [self.header, self.keywords, self.meetup]

    # date=2019/02/21, start_time=7:00pm, duration=2h
    def readable_datetime(self, schedule):
        start_time = datetime.fromtimestamp(schedule.start_at)
        date = datetime.strptime(start_time, '%Y/%m/%d')
        weekday = calendar.day_name[date.weekday()]
        readable_date = '{}, {}'.format(weekday, date.strftime("%B %d, %Y"))

        end_time = start_time + timedelta(0, schedule.duration * 60)
        readable_time = '{}-{}'.format(start_time.strftime('%I:%M'),
                              end_time.strftime('%I:%M %p'))
        return [readable_date, readable_time]

    def draw_schedule(self, schedule):
        self.draw_text(self.datetime,
                       self.readable_datetime(schedule),
                       self.txt_style['datetime'])
        self.imgs.append(self.datetime)

        address = [schedule.address1, schedule.location]
        self.draw_text(self.location, address, self.txt_style['address'])
        self.imgs.append(self.location)

    def draw_speaker(self, presenter):
        title = self.get_template('title.png')
        self.draw_text(title, ['Presenter'], self.txt_style['title'])

        content = self.get_template('content.png')
        avatar = self.get_avatar(presenter)
        composer = ImageComposer([content, avatar])
        composer.zstack(self.img_style['avatar']['box'],
                        self.img_style['avatar']['align'])
        self.draw_text(content,
                       [presenter.full_name],
                       self.txt_style['presenter_name'])
        self.draw_text(content,
                       [presenter.title, presenter['company/organization']],
                       self.txt_style['presenter_title'])

        self.draw_text(content,
                       [presenter.self_intro],
                       self.txt_style['presenter_introduction'])

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

        self.draw_text(content,
                       [project['short_description']],
                       self.txt_style['project_description'])
        self.imgs.extend([title, content])

    def draw_session(self, session):
        content = self.get_template('content.png')
        self.draw_text(content,
                       [session.name],
                       self.txt_style['session_name'])
        self.draw_text(content,
                       [session.highlight or session.summary],
                       self.txt_style['session_summary'])
        self.imgs.append(content)

    def draw(self, session, presenter):
        self.reset()
        self.draw_session(session)
        self.draw_schedule(session.schedule)
        self.draw_speaker(presenter)
        self.draw_project(presenter.project)
#        self.imgs.append(self.tail)

    def process(self, args):
        session = self.get_session(args.session)
        presenter = self.get_presenter(session.presenter)
        self.draw(session, presenter)
        composer = ImageComposer(self.imgs)
        composer.vstack()
        self.save(composer, filename='session', upload=True)
