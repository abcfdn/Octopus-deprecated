# -*- encoding: UTF-8 -*-

import re
import requests


class Meetup:
    URL_NAME = 'ABC-Blockchain-Community-Meetup'
    EVENT_URL = 'https://api.meetup.com/{}/events'.format(URL_NAME)

    def __init__(self, api_key):
        self.api_key = api_key

    # url example:
    # https://www.meetup.com/ABC-Blockchain-Community-Meetup/events/258181315/
    def get_event_from_url(self, url):
        m = re.search('events\/(\d+)', url)
        return self.get_event(m.group(1)) if m else None

    def get_event(self, event_id):
        return requests.get(self._event_url(event_id)).json()

    # start_datetime is millionseconds starting from epoch
    def get_events(self, no_earlier_than, no_later_than):
        params = {
            'no_earlier_than': no_earlier_than.isoformat(),
            'no_later_than': no_later_than.isoformat(),
        }
        return requests.get(self._events_url(params)).json()

    def update_event(self, event_id, payload):
        return requests.patch(self._event_url(event_id), payload).json()

    def create_event(self, payload):
        return requests.post(self._events_url(), payload).json()

    def _event_url(self, event_id, params={}):
        return '{}/{}?{}'.format(self.EVENT_URL, event_id, self._query(params))

    def _events_url(self, params={}):
        return '{}?{}'.format(self.EVENT_URL, self._query(params))

    def _query(self, params):
        params.update({'key' : self.api_key})
        return '&'.join(['{}={}'.format(k, v) for k,v in params.items()])
