# -*- encoding: UTF-8 -*-

import requests


class Meetup:
    URL_NAME = 'ABC-Blockchain-Community-Meetup'
    EVENT_URL = 'https://www.meetup.com/{}/events'.format(URL_NAME)

    DEFAULT_VALUES = {
        'publish_status': 'draft',
        'duration': '540000',
    }
    FILEDS = ['name', 'description', 'time', 'duration', 'publish_status',
              'how_to_find_us', 'publish_status']

    def __init__(self, api_key):
        self.api_key = api_key

    # start_datetime is millionseconds starting from epoch
    def get_events(self, start_datetime):
        params = {
            'no_earlier_than': start_datetime.isoformat(),
            'no_later_than': start_datetime.isoformat()
        }
        response = self.run_query(start_datetime)
        print(response)

    def run_query(self, params):
        return requests.get(self._url(params), allow_redirects=True)

    def _url(self, params):
        return '{}?{}'.format(EVENT_URL, self._query(params))

    def _query(self, params):
        params.update({'api_key' : self.api_key})
        return '&'.join(['{}={}'.format(k, v) for k,v in params.items()])
