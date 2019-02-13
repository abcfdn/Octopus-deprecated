# -*- encoding: UTF-8 -*-

import os

from toolset.google.drive import GoogleDrive
import toolset.utils.util as util

from constants import TASK_CONFIG_ROOT_PATH


class Resource:
    def __init__(self, google_config, data_config):
        self.drive_service = GoogleDrive(google_config)
        self.sync_to_local(data_config)

    def sync_to_local(self, data_config):
        for resource in data_config.values():
            if 'local' in resource:
                util.create_if_not_exist(resource['local'])
                if 'remote' in resource:
                    self.drive_service.sync_folder(resource['remote'],
                                                   resource['local'])


class Task(Resource):
    def __init__(self, common_config):
        task_config = self.load_task_config()
        super().__init__(common_config['google'], task_config['data'])
        util.deepmerge(task_config, common_config)
        self.config = common_config

    def load_task_config(self):
        task_config_file = os.path.join(
            TASK_CONFIG_ROOT_PATH,
            '{}.yaml'.format(self.__class__.__name__))
        return util.load_yaml(task_config_file)

    def process(self, args):
        raise("Not Implemented")


class Workflow:
    def __init__(self, tasks):
        self.tasks = tasks

    def run(self, args):
        for task in self.tasks:
            task.process(args)


