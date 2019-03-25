# -*- encoding: UTF-8 -*-

from bson.objectid import ObjectId
from datetime import datetime

from .schema import SessionSchema, PresenterSchema, PhotoSchema, MemberSchema
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

    def get_member(self, email):
        member = self.member_store.find({'email': email})
        return self.dump_member(member)

    def get_members(self):
        members = self.member_store.find_all({})
        return [self.dump_member(m) for m in members]

    def get_presenter(self, email):
        presenter = self.presenter_store.find({'email': email})
        return self.dump_presenter(presenter)

    def store_photo(self, data):
        return self.picture_store.create(self.dump_picture(data))

    def get_photo(self, photo_id):
        picture = self.picture_store.find({'photo_id': photo_id})
        return self.dump_picture(picture)

    def get_credential(self, session_id):
        return self.credential_store.find({'_id': ObjectId(session_id)})

    def get_credential_by_token(self, token):
        return self.credential_store.find({'credentials.token': token})

    def create_session(self, session):
        return str(self.credential_store.create(session))

    def dump_session(self, data):
       return SessionSchema(exclude=['_id']).dump(data).data

    def dump_presenter(self, data):
       return PresenterSchema(exclude=['_id']).dump(data).data

    def dump_picture(self, data):
       return PhotoSchema(exclude=['_id']).dump(data).data

    def dump_member(self, data):
       return MemberSchema(exclude=['_id']).dump(data).data
