# -*- encoding: UTF-8 -*-

from toolset.mongo import MongoClient


class EventStore(Task):
    def __init__(self):
        self.mongo = MongoClient(config['mongo'])
