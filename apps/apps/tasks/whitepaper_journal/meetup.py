# -*- encoding: UTF-8 -*-

import os
import logging

from datetime import timedelta, timezone
from toolset.meetup import Meetup
import toolset.utils.util as util
from .base import WhitepaperJournalBase

logger = logging.getLogger('whitepaper_journal_meetup')


class WhitepaperJournalMeetup(WhitepaperJournalBase):

    def __init__(self, common_config):
        super().__init__(common_config)
        self.meetup_service = Meetup(self.get_api_key())

    def get_api_key(self):
        meetup_config = util.load_yaml(self.config['meetup']['api_key'])
        return meetup_config['api_key']

    @classmethod
    def add_parser(cls, parser):
        meetup_parser = parser.add_parser(
            cls.__name__, help='create/update meetup event')
        group = meetup_parser.add_mutually_exclusive_group()
        group.add_argument('--event',
                           help='event_id, which is presenter name + date')

    def is_equal(self, event, meetup_event):
        # compare location
        site = event['schedule']['site'].strip().lower()
        venue_id = self.config['meetup']['venue_id'][site]
        name = meetup_event['name'].strip().lower()
        return meetup_event['venue']['id'] == venue_id and (
            meetup_event['name'].strip().lower().startswith(name) or
            meetup_event['name'].strip().lower().endswith(name))

    def search_meetup_event(self, event):
        event_start_time = self.event_start_time(event)
        # loose the constraints in case the start time is wrong
        no_earlier_than = event_start_time - timedelta(0, 3600)
        no_later_than = event_start_time + timedelta(0, 3600)
        candidates = self.meetup_service.get_events(no_earlier_than, no_later_than)
        for candidate in candidates:
            if self.is_equal(event, candidate):
                return candidate
        return None

    def generate_link(self, name, url):
        return '{0}: <a href="{1}" class="linkified">{1}</a>'.format(name, url)

    def generate_materials(self, event):
        lines = []
        fields = [('Project Website', 'website'),
                  ('Deck File', 'deck_file_link')]
        for field in fields:
            if field[1] in event and event[field[1]]:
                lines.append(self.generate_link(field[0], event[field[1]]))
        if lines:
            return '<br/>'.join(lines)
        return 'None'

    def load_description(self):
        localdir = self.config['data']['template']['local']
        description_file = os.path.join(localdir, 'description.html')
        return open(description_file, 'r').read()

    def text_to_html(self, text):
        lines = text.split('\n')
        return '<br/>'.join(lines)

    def generate_description(self, event):
        livestream = self.generate_link('Livestream', event['schedule']['livestream'])
        summary = self.text_to_html(event['summary'])
        presenter = '{}, {} at {}'.format(event['presenter_name'],
                                          event['title'],
                                          event['company/organization'])
        self_introdution = self.text_to_html(event['self-introduction'])

        return self.load_description() \
                .replace('\n', ' ') \
                .replace('##SUMMARY##', summary) \
                .replace('##SPEKAER_NAME##', presenter) \
                .replace('##SPEKAER_INTRODUCTION##', self_introdution) \
                .replace('##GOTOMEETING##', livestream) \
                .replace('##MATERAILS##', self.generate_materials(event)) \

    def get_venue_id(self, event):
        site = event['schedule']['site'].strip().lower()
        return self.config['meetup']['venue_id'][site]

    def get_session_name(self, name):
        long_name = name + ' - ABC Whitepaper Journal'
        return name if len(long_name) > 80 else long_name

    def create_payload(self, event):
        payload = {}
        payload['name'] = self.get_session_name(event['session_name'])
        payload['description'] = self.generate_description(event)
        payload['how_to_find_us'] = self.config['meetup']['how_to_find_us']
        payload['time'] = (int)(self.event_start_time(event).timestamp() * 1000)
        payload['duration'] = self.duration_as_sec(
            event['schedule']['duration']) * 1000
        payload['venue_id'] = self.get_venue_id(event)
        payload['featured_photo_id'] = self.config[
            'meetup']['featured_photo_id']['default']
        payload['rsvp_limit'] = self.config['meetup']['rsvp_limit']
        return payload

    def create_event(self, event):
        payload = self.create_payload(event)
#        response = self.meetup_service.update_event(meetup_event['id'], payload)
#        return response

    def update_event(self, event, meetup_event):
        payload = self.create_payload(event)
        logger.info('Updating event {} with payload {}'.format(
            meetup_event['id'], payload))
        self.meetup_service.update_event(meetup_event['id'], payload)

    def process(self, args):
        event = self.get_event(args.event)
        if event['schedule']['meetup']:
            meetup_event = self.meetup_service.get_event_from_url(
                    event['schedule']['meetup'])
            self.update_event(event, meetup_event)
        else:
            self.create_event(event)
