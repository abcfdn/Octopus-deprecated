# -*- encoding: UTF-8 -*-

import logging

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

    def process(self, args):
        event = self.get_event(args.event)
        event_time = self.get_start_datetime(event['schedule']['date'],
                                             event['schedule']['start_time'])
        self.meetup_service.get_events(event_time)
