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
        for key, resource in data_config.items():
            if key == 'output':
                continue
            if 'local' in resource:
                util.create_if_not_exist(resource['local'])
                if 'remote' in resource:
                    self.drive_service.sync_folder(resource['remote'],
                                                   resource['local'])


class Task(Resource):
    def __init__(self, common_config):
        task_config = self.load_config()
        self.config = util.deepmerge(task_config, common_config)
        super().__init__(self.config['google'], self.config['data'])

    def app_name(self):
        raise('Not Implemented')

    def load_config(self):
        task_common_config = self.load_task_common_config()
        task_config_file = os.path.join(
            TASK_CONFIG_ROOT_PATH,
            self.app_name(),
            '{}.yaml'.format(self.__class__.__name__))
        task_config = util.load_yaml(task_config_file)
        return util.deepmerge(task_config, task_common_config)

    def load_task_common_config(self):
        config_file = os.path.join(
            TASK_CONFIG_ROOT_PATH, self.app_name(), 'common.yaml')
        return util.load_yaml(config_file)

    def process(self, args):
        raise("Not Implemented")


class Workflow:
    def __init__(self, tasks):
        self.tasks = tasks

    def run(self, args):
        for task in self.tasks:
            task.process(args)


