# -*- encoding: UTF-8 -*-

import os
import sys

import logging
import json

import server.platforms.utils.util as util
from server.platforms.google.sheet import GoogleSheet
from server.platforms.google.photo import GooglePhoto
from server.db.mongo import MongoConnection, MemberStore
from server.workflow.base import Task

from google.oauth2 import service_account
from .card import MembershipCard

from server.workflow.constants import MEMBERSHIP_APP

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.yaml')

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('app')


class MemberSync(Task):
    NUM_OF_ROWS_TO_READ = 1000
    FIELDS_TO_COMPARE = ['session_name', 'presenter_name']

    def __init__(self, google_creds, mongo_config):
        super().__init__(google_creds)
        self.sheet_service = GoogleSheet(google_creds)
        self.load_members()
        self.card_generator = MembershipCard(google_creds)
        self.photo_service = GooglePhoto(google_creds)
        self.member_store = MemberStore(MongoConnection(mongo_config))

    def app_name(self):
        return MEMBERSHIP_APP

    def preprocess(self, member):
        member['started_at'] = util.to_epoch_time(member['timestamp'])
        key = 'do_you_want_be_a_volunteer_for_future_abc_events_?'
        volunteer = member.get(key, 'No')
        member['volunteer_candidate'] = volunteer.lower().startswith('yes')
        return self.transform_one(member)

    def sync(self):
        to_insert = []
        for member in self.members:
            member = self.preprocess(member)
            existing_member = self.member_store.find({'email': member['email']})
            if not existing_member:
                to_insert.append(member)
        print("Will insert {} among {} members".format(len(to_insert), len(self.members)))
        self.add_membership_card(to_insert)
        for member in to_insert:
            print('Inserting {}'.format(member))
            self.member_store.create(member)

    def get_base_url(self, photo_id):
        result = self.photo_service.get_photo(photo_id)
        return json.loads(result).get('baseUrl', '')

    def add_membership_card(self, members):
        filepath2member = {}
        for member in members:
            filepath = self.card_generator.process(member)
            filepath2member[filepath] = member
        token2filepath = self.photo_service.upload(filepath2member.keys())
        results = self.photo_service.batch_create_items(list(token2filepath.keys()))
        print(len(results))
        for result in results:
            token = result['uploadToken']
            member = filepath2member[token2filepath[token]]
            member['membership_card'] = {
                'filename': result['mediaItem']['filename'],
                'photo_id': result['mediaItem']['id'],
                'base_url': result['mediaItem'].get('baseUrl', '') or self.get_base_url(result['mediaItem']['id']),
                'product_url': result['mediaItem']['productUrl'],
                'upload_token': token
            }

    def load_members(self):
        self.members = self.sheet_service.read_as_map(
            self.config['data']['member']['remote'],
            'Form Responses 1',
            (2, self.NUM_OF_ROWS_TO_READ + 1))

    def transform_one(self, doc):
        return {
            dst: doc[src]
            for src, dst in self.config['fields']['member'].items()
            if (src in doc and doc[src])
        }
