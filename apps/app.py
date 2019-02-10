# -*- encoding: UTF-8 -*-

import yaml

class App:
    CONFIG_FILE = 'config.yaml'

    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        with open(self.CONFIG_FILE, 'r') as f:
            return yaml.load(f)

    def run(self):
        raise("Not Implemented")
