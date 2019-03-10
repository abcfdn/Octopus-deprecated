# -*- encoding: UTF-8 -*-

from pymongo import MongoClient


class MongoStore:
    DATABASE = 'octopus'

    def __init__(self, config):
        conn = MongoClient(self.mongo_url(config))
        self.db = conn.get_database()
        self.coll = self.db[self.get_coll_name()]

    def get_coll_name(self):
        raise "Not Implemented"

    def get_db(self, config):

    def mongo_url(self, config):
        return "mongodb://{}:{}@{}:{}/{}".format(
            config['username'], config['password'],
            config['host'], config['port'], self.DATABASE)

    def find_all(self, selector):
       return self.coll.find(selector)

     def find(self, selector):
       return self.coll.find_one(selector)

     def create(self, kudo):
       return self.coll.insert_one(kudo)

     def update(self, selector, doc):
       return self.coll.replace_one(selector, doc).modified_count

     def delete(self, selector):
       return self.coll.delete_one(selector).deleted_count


class EventStore(MongoStore):
     def get_coll_name(self):
         return "event"


class SessionStore(MongoStore):
     def get_coll_name(self):
         return "session"


class ProjectStore(MongoStore):
     def get_coll_name(self):
         return "project"


class PresenterStore(MongoStore):
     def get_coll_name(self):
         return "presenter"
