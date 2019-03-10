# -*- encoding: UTF-8 -*-

from pymongo import MongoClient
import urllib.parse


class MongoConnection:
    def __init__(self, config):
        self.conn = MongoClient(self.mongo_url(config))

    def mongo_url(self, config):
        return "mongodb://{}:{}@{}:{}/{}".format(
            urllib.parse.quote_plus(config['username']),
            urllib.parse.quote_plus(config['password']),
            config['host'], config['port'], config['database'])

    def get_database(self):
        return self.conn.get_database()


class MongoStore:
    def __init__(self, conn):
        self.db = conn.get_database()
        self.coll = self.db[self.get_coll_name()]

    def get_coll_name(self):
        raise "Not Implemented"

    def find_all(self, selector):
        return self.coll.find(selector)

    def find(self, selector):
        return self.coll.find_one(selector)

    def create(self, doc):
        return self.coll.insert_one(doc).inserted_id

    def replace(self, selector, doc):
        return self.coll.replace_one(selector, doc).modified_count

    def update(self, selector, doc):
        return self.coll.update_one(selector, doc).modified_count

    def delete(self, selector):
        return self.coll.delete_one(selector).deleted_count


class SessionStore(MongoStore):
    def get_coll_name(self):
        return "session"


class PresenterStore(MongoStore):
    def get_coll_name(self):
        return "presenter"


class TopicStore(MongoStore):
    def get_coll_name(self):
        return "topic"
