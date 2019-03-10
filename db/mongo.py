# -*- encoding: UTF-8 -*-

from pymongo import MongoClient


class MongoEventStore:
    def __init__(self, config):
        conn = MongoClient(self.mongo_url(config))
        self.db = conn.get_database()
        self.coll = self.db[config['collection']]

    def mongo_url(self, config):
        return "mongodb://{}:{}@{}:{}/{}".format(
            config['username'], config['password'],
            config['host'], config['port'], config['database'])

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
