# -*- encoding: UTF-8 -*-

from datetime import datetime

from .schema import SessionSchema, PresenterSchema
from .mongo import MongoConnection, PresenterStore, SessionStore

class Service(object):
    def __init__(self, config):
        conn = MongoConnection(config)
        self.session_store = SessionStore(conn)
        self.presenter_store = PresenterStore(conn)

    def get_sessions(self, start_time, end_time):
        selector = {
            '$and': [
                {'schedule.start_at': {'$gte': start_time}},
                {'schedule.start_at': {'$lte': end_time}}
            ]
        }
        sessions = self.session_store.find_all(selector)
        return [self.dump_session(s) for s in sessions]

    def get_past_sessions(self):
        end_time = int(datetime.now().timestamp())
        start_time = end_time - 15552000 # 180 days
        return self.get_sessions(start_time, end_time)

    def get_future_sessions(self):
        start_time = int(datetime.now().timestamp())
        end_time = start_time + 15552000 # 180 days
        return self.get_sessions(start_time, end_time)

    def get_recent_sessions(self):
        now = int(datetime.now().timestamp())
        return self.get_sessions(now - 2592000, now + 2592000)

    def get_session(self, created_at):
        sesssion = self.session_store.find_all({'created_at': created_at})
        return self.dump_session(session)

    def get_presenter(self, email):
        presenter = self.presenter_store.find({'email': email})
        return self.dump_presenter(presenter)

    def dump_session(self, data):
       return SessionSchema(exclude=['_id']).dump(data).data

    def dump_presenter(self, data):
       return PresenterSchema(exclude=['_id']).dump(data).data
