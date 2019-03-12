# -*- encoding: UTF-8 -*-

import os
import sys
sys.path.append("..")

import logging
import dateparser

from bson.objectid import ObjectId

import server.platforms.utils.util as util
from server.platforms.google.sheet import GoogleSheet
from server.db.mongo import MongoConnection, SessionStore, PresenterStore

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.yaml')

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('app')


def duration_as_mins(duration):
    for i,c in enumerate(duration):
        if not c.isdigit():
            break
    number=int(duration[:i])
    unit=duration[i:].strip().lower()

    if unit == 'h' or unit.startswith('hour'):
        return number * 60
    elif unit == 'm' or unit.startswith('min'):
        return number
    elif unit == 's' or unit.startswith('sec'):
        return number / 60
    elif unit == 'd' or unit.startswith('day'):
        return number * 60 * 24
    else:
        logger.warning('Unrecognized duration')
        return -1

def to_epoch_time(time):
    return (int)(dateparser.parse(time).timestamp())

class DataSync:
    NUM_OF_ROWS_TO_READ = 1000
    FIELDS_TO_COMPARE = ['session_name', 'presenter_name']

    def __init__(self, common_config):
        self.config = util.load_yaml(CONFIG_PATH)
        self.config.update(common_config)

        self.sheet_service = GoogleSheet(self.config['google'])
        self.load_events()
        self.load_schedules()

        conn = MongoConnection(self.config['mongo'])
        self.session_store = SessionStore(conn)
        self.presenter_store = PresenterStore(conn)

    def preprocess_event(self, event):
        event['duration_as_mins'] = duration_as_mins(
            event['duration'])
        event['created_at'] = to_epoch_time(event['timestamp'])

    def preprocess_schedule(self, schedule):
        date_time = '{} {} PST'.format(
            schedule['date'], schedule['start_time'])
        schedule['start_at'] = to_epoch_time(date_time)
        schedule['duration_as_mins'] = duration_as_mins(
            schedule['duration'])

    def compare_and_update(self, updated, selector, mongo_store):
        result = mongo_store.find(selector)
        if not result:
            print('Inserting {}'.format(updated))
            return mongo_store.create(updated)
        need_update = False
        for k, v in updated.items():
            existing_v = result.get(k, None)
            if type(existing_v) is dict:
                if type(v) is dict:
                    for vk, vv in v.items():
                        if existing_v.get(vk, None) != vv:
                            need_update = True
                else:
                    need_update = True
            elif existing_v != v:
                need_update = True
                break
        if need_update:
            result = util.deepmerge(updated, result)
            print('Updating {} to {}'.format(selector, result))
            mongo_store.replace(selector, result)
            return result['_id']

    def sync(self):
        for event in self.events:
            self.preprocess_event(event)
            self.sync_one(event)

    def sync_one(self, event):
        project = self.transform_one('project', event)
        presenter = self.transform_one('presenter', event)
        presenter['project'] = project
        self.compare_and_update(
            presenter,
            {
                'email': presenter['email']
            },
            self.presenter_store)

        session = self.transform_one('session', event)
        session['presenter'] = presenter['email']
        schedule = self.select_schedule(session['created_at'])
        if schedule:
            self.preprocess_schedule(schedule)
            schedule = self.transform_one('session_schedule', schedule)
            session['schedule'] = schedule
        self.compare_and_update(
            session,
            {'created_at': session['created_at']},
            self.session_store)

    def select_schedule(self, session_id):
        for schedule in self.schedules:
            if str(schedule.get('session_id', '')) == str(session_id):
                return schedule
        return None

    def load_events(self):
        self.events = self.sheet_service.read_as_map(
            self.config['data']['event']['remote'],
            'Form Responses 1',
            (2, self.NUM_OF_ROWS_TO_READ + 1))

    def load_schedules(self):
        self.schedules = self.sheet_service.read_as_map(
            self.config['data']['schedule']['remote'],
            'Schedule',
            (2, self.NUM_OF_ROWS_TO_READ + 1))
        self.schedules.sort(key=lambda k: k['date'])

    def transform_one(self, coll, doc):
        return {
            dst: doc[src]
            for src, dst in self.config['fields'][coll].items()
            if (src in doc and doc[src])
        }
