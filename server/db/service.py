# -*- encoding: UTF-8 -*-

from bson.objectid import ObjectId
from datetime import datetime

from .schema import SessionSchema, PresenterSchema, MemberSchema
from .mongo import MongoConnection, PresenterStore, SessionStore, PictureStore, CredentialStore, MemberStore

class Service(object):
    def __init__(self, config):
        conn = MongoConnection(config)
        self.session_store = SessionStore(conn)
        self.presenter_store = PresenterStore(conn)
        self.picture_store = PictureStore(conn)
        self.credential_store = CredentialStore(conn)
        self.member_store = MemberStore(conn)

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
        session = self.session_store.find({'created_at': created_at})
        return self.dump_session(session)

    def get_candidate_sessions(self):
        selector = { "schedule" : { "$exists" : False } }
        sessions = self.session_store.find_all(selector)
        return [self.dump_session(s) for s in sessions]

    def get_member(self, email):
        member = self.member_store.find({'email': email})
        return self.dump_member(member)

    def set_member(self, selector, fieldname, fieldvalue):
        self.member_store.update_one(
            selector, {'$set': {fieldname: fieldvalue}})

    def get_members(self):
        members = self.member_store.find_all({}, max_cnt=1000)
        return [self.dump_member(m) for m in members]

    def get_presenter(self, email):
        presenter = self.presenter_store.find({'email': email})
        return self.dump_presenter(presenter)

    def get_credential(self, user, source):
        return self.credential_store.find({'user': user, 'source': source})

    def create_credential(self, creds):
        self.credential_store.create(creds)

    def dump_session(self, data):
       return SessionSchema(exclude=['_id']).dump(data).data

    def dump_presenter(self, data):
       return PresenterSchema(exclude=['_id']).dump(data).data

    def dump_member(self, data):
       return MemberSchema(exclude=['_id']).dump(data).data
