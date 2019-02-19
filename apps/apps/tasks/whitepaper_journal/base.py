# -*- encoding: UTF-8 -*-

import calendar
import dateparser
from datetime import datetime, timedelta

from apps.base import Task
from apps.constants import WHITEPAPER_JOURNAL_APP
from toolset.google.sheet import GoogleSheet


class WhitepaperJournalBase(Task):
    NUM_OF_ROWS_TO_READ = 1000
    FIELDS_TO_COMPARE = ['session_name', 'presenter_name']

    def __init__(self, common_config):
        super().__init__(common_config)
        self.load_schedule_and_events()

    def load_schedule_and_events(self):
        sheet_service = GoogleSheet(self.config['google'])
        self.schedules = sheet_service.read_as_map(
            self.config['data']['schedule']['remote'],
            'Schedule',
            (2, self.NUM_OF_ROWS_TO_READ + 1))
        self.schedules.sort(key=lambda k: k['date'])

        self.events = sheet_service.read_as_map(
            self.config['data']['event']['remote'],
            'Form Responses 1',
            (2, self.NUM_OF_ROWS_TO_READ + 1))

    def app_name(self):
        return WHITEPAPER_JOURNAL_APP

    def duration_as_sec(self, duration):
        for i,c in enumerate(duration):
            if not c.isdigit():
                break
        number=int(duration[:i])
        unit=duration[i:].lower()

        if unit == 'h':
            return number * 3600
        elif unit == 'min' or unit == 'm':
            return number * 60
        elif unit == 'sec' or unit == 's':
            return number
        raise('Unrecognized duration')

    def to_datetime(self, date, time):
        date_time = '{} {} PST'.format(date, time)
        return dateparser.parse(date_time)

    def event_start_time(self, event):
        return self.to_datetime(event['schedule']['date'],
                                event['schedule']['start_time'])

    def event_end_time(self, event):
        start_time = self.event_start_time(event)
        return start_time + timedelta(0, self.duration_as_sec(
            event['schedule']['duration']))

    # date=2019/02/21, start_time=7:00pm, duration=2h
    def readable_time(self, event):
        return '{}-{}'.format(self.event_start_time(event).strftime('%I:%M'),
                              self.event_end_time(event).strftime('%I:%M %p'))

    def readable_date(self, date):
        date = datetime.strptime(date, '%Y/%m/%d')
        weekday = calendar.day_name[date.weekday()]
        return '{}, {}'.format(weekday, date.strftime("%B %d, %Y"))

    def get_event_id(self, event):
        event_date = event['date'].replace('/', '')
        return '{}{}'.format(event_date, event['site'])

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

    def process(self, args):
        raise('Not Implemented')
